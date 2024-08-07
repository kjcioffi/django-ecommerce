import json
from typing import Any
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import stripe
import environ

from django.contrib.sessions.backends.db import SessionStore

from store.forms import OrderAdminForm, OrderForm, ProductAdminForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from store.models import Order, OrderItem, Product, Store
from django.contrib.auth.mixins import LoginRequiredMixin

from store.view_utils import (
    ReportingMixin,
    create_orders_for_stores,
    fetch_products_and_store_objects_after_payment,
    get_order_items_by_store,
    get_order_items_from_stripe,
    get_products_and_quantities_from_bag,
)

env = environ.Env()

stripe.api_key = env("STRIPE_API_KEY")
stripe_webhook_key: str = env("STRIPE_WEBHOOK_KEY")


class StoreProducts(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/store_products.html"

    def get_queryset(self) -> QuerySet[Product]:
        store_id = self.kwargs.get("store_id")
        queryset = Product.objects.filter(store=store_id)
        return queryset


class StoreList(ListView):
    model = Store
    context_object_name = "stores"
    template_name = "store/store_list.html"


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/product_detail.html"


def checkout(request):
    # populate products in the purchase summary of the web page
    products_in_bag = get_products_and_quantities_from_bag(request)

    # context item for customer to view when placing order.
    total_cost = sum(
        bag_item["product"].price * bag_item["quantity"] for bag_item in products_in_bag
    )

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            stores = get_order_items_by_store(products_in_bag)
            order_info = form.cleaned_data
            order_info["session_key"] = request.session.session_key

            if stripe.api_key:
                return create_payment_session(request, order_info, products_in_bag)
            else:
                create_orders_for_stores(stores, order_info)
    else:
        form = OrderForm()

    return render(
        request,
        "store/checkout.html",
        {"form": form, "products_in_bag": products_in_bag, "total_cost": total_cost},
    )


def create_payment_session(request, order_info: dict, order_items: list):
    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"{order_item["product"].name} ({order_item["product"].store.name})",
                },
                "unit_amount": int(
                    order_item["product"].price * 100
                ),  # Convert to cents
            },
            "quantity": order_item["quantity"],
        }
        for order_item in order_items
    ]

    # Serialize order_items to include only necessary attributes
    serialized_order_items = [
        {
            "product_id": order_item["product"].id,
            "product_name": order_item["product"].name,
            "store_id": order_item["product"].store.id,
            "price": str(order_item["product"].price),
            "quantity": order_item["quantity"],
        }
        for order_item in order_items
    ]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri(reverse("store:store_list")),
            cancel_url=request.build_absolute_uri(reverse("store:checkout")),
            customer_email=order_info["email"],
            metadata={
                "first_name": order_info["first_name"],
                "last_name": order_info["last_name"],
                "email": order_info["email"],
                "phone_number": order_info["phone_number"],
                "street": order_info["street"],
                "zip": order_info["zip"],
                "city": order_info["city"],
                "state": order_info["state"],
                "session_key": order_info["session_key"],
                "order_items": json.dumps(serialized_order_items),
            },
        )

        return redirect(session.url, code=303)

    except stripe.error.InvalidRequestError as e:
        print(f"Stripe error: {e}")
        messages.add_message(
            request,
            messages.ERROR,
            "There was an error with your payment. Please try again.",
        )
        return redirect("store:checkout")

    except Exception as e:
        print(f"Unexpected error: {e}")
        messages.add_message(
            request,
            messages.ERROR,
            "An unexpected error occurred. Please try again later.",
        )
        return redirect("store:checkout")


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe_webhook_key)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session["metadata"]
        order_items = json.loads(metadata["order_items"])

        stores = fetch_products_and_store_objects_after_payment(
            get_order_items_from_stripe(order_items)
        )

        create_orders_for_stores(
            stores,
            first_name=metadata["first_name"],
            last_name=metadata["last_name"],
            email=metadata["email"],
            phone_number=metadata["phone_number"],
            street=metadata["street"],
            zip=metadata["zip"],
            city=metadata["city"],
            state=metadata["state"],
        )

        # assign the current request session to the user's and not Stripe.
        request.session = SessionStore(session_key=metadata["session_key"])
        request.session["bag"] = []
        request.session["total_items"] = 0
        request.session.save()

    return HttpResponse(status=200)


@require_http_methods(["POST"])
def add_to_bag(request) -> JsonResponse:
    """
    Process information from client-side interactions then \
    send the total number of items in the bag.

    Keeps count of different products added and their quantities.
    """
    product_id = int(request.POST.get("product_id"))

    if not isinstance(product_id, int):
        raise TypeError("Product ID must be an integer.")

    bag: list = request.session.get("bag", [])

    product_found = False
    for product in bag:
        if product["product_id"] == product_id:
            product["quantity"] += 1
            product_found = True
            break

    if not product_found:
        bag.append({"product_id": product_id, "quantity": 1})

    request.session["bag"] = bag

    total_items = sum(product["quantity"] for product in bag)
    request.session["total_items"] = total_items

    return JsonResponse({"status": "success", "total_items": total_items})


class ProductAdmin(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/user-admin/product/product_admin.html"
    login_url = "/accounts/login"

    def get_queryset(self) -> QuerySet[Product]:
        # return products only from the store they own
        store = Store.objects.for_user_admin(self.request.user)
        return Product.objects.filter_by_store(store)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["store"] = Store.objects.for_user_admin(owner=self.request.user)
        return context


@login_required
def product_admin_modify(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.store.owner != request.user:
        return HttpResponseForbidden("You don't have permission to modify this product.")
    
    form = ProductAdminForm(instance=product)

    if request.method == "POST":
        form = ProductAdminForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            if "update" in request.POST:
                form.save()
                messages.add_message(
                    request,
                    messages.INFO,
                    f"{product.name}({product.pk}) successfully saved.",
                )
            elif "delete" in request.POST:
                product.delete()
                messages.add_message(
                    request,
                    messages.INFO,
                    f"{product.name}(ID {product.pk}) successfully deleted.",
                )
            return HttpResponseRedirect(reverse("store:product_admin"))

    return render(request, "store/user-admin/product/product_admin_modify.html", {"form": form})


class ProductAdminAdd(LoginRequiredMixin, CreateView):
    form_class = ProductAdminForm
    template_name = "store/user-admin/product/product_admin_add.html"
    success_url = reverse_lazy("store:product_admin")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.store = Store.objects.get(owner=self.request.user)
        product.save()
        return super().form_valid(form)


class OrderAdmin(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "store/user-admin/order/order_admin.html"
    login_url = "/accounts/login"

    def get_queryset(self) -> QuerySet[Product]:
        # return orders only from the store they own
        store = Store.objects.for_user_admin(self.request.user)
        return Order.objects.filter_by_store(store)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["store"] = Store.objects.for_user_admin(owner=self.request.user)
        return context


@login_required
def order_admin_modify(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if order.store.owner != request.user:
        return HttpResponseForbidden("You don't have permission to modify this order.")

    form: ModelForm = OrderAdminForm(instance=order)

    if request.method == "POST":
        form: ModelForm = OrderAdminForm(request.POST, instance=order)

        if form.is_valid():
            if "update" in request.POST:
                form.save()
                messages.add_message(
                    request,
                    messages.INFO,
                    f"Order from {order.first_name} {order.last_name} (ID {order.pk}) successfully saved.",
                )
            elif "delete" in request.POST:
                order.delete()
                messages.add_message(
                    request,
                    messages.INFO,
                    f"Order from {order.first_name} {order.last_name} (ID {order.pk}) successfully deleted.",
                )
            return HttpResponseRedirect(reverse("store:order_admin"))

    return render(
        request, "store/user-admin/order/order_admin_modify.html", {"form": form, "order": order}
    )


class DownloadCustomerReport(LoginRequiredMixin, ReportingMixin, View):
    def get(self, request, *args, **kwargs):
        store = Store.objects.for_user_admin(self.request.user)
        orders: QuerySet[Order] = Order.objects.filter(store=store)

        header = ["Store", "First Name", "Last Name", "Email", "Phone Number"]
        data = [
            (
                order.store,
                order.first_name,
                order.last_name,
                order.email,
                order.phone_number,
            )
            for order in orders
        ]
        current_datetime = timezone.now()
        str_datetime = current_datetime.strftime("%d_%m_%Y_%H:%M:%S")

        return self.generate_csv_report(f"customer_list_{str_datetime}", header, data)


class DownloadCustomerPDFReport(LoginRequiredMixin, ReportingMixin, View):
    def get(self, request, *args, **kwargs):
        store = Store.objects.for_user_admin(self.request.user)
        orders: QuerySet[Order] = Order.objects.filter(store=store)

        data = {
            "store": store,
            "customers": orders
        }

        current_datetime = timezone.now()
        str_datetime = current_datetime.strftime("%d_%m_%Y_%H:%M:%S")

        return self.generate_pdf_report(f"customer_list_{str_datetime}", "store/reports/customer.html", data)


class DownloadProductReport(LoginRequiredMixin, ReportingMixin, View):
    def get(self, request, *args, **kwargs):
        store = Store.objects.for_user_admin(self.request.user)
        products: QuerySet[Product] = Product.objects.filter(store=store)

        header = ["store", "name", "rating", "price", "description"]
        data = [
            (
                product.store,
                product.name,
                product.rating,
                product.price,
                product.description
            )
            for product in products
        ]
        current_datetime = timezone.now()
        str_datetime = current_datetime.strftime("%d_%m_%Y_%H:%M:%S")

        return self.generate_csv_report(f"product_list_{str_datetime}", header, data)
    

class DownloadProductPDFReport(LoginRequiredMixin, ReportingMixin, View):
    def get(self, request, *args, **kwargs):
        store = Store.objects.for_user_admin(self.request.user)
        products: QuerySet[Product] = Product.objects.filter(store=store)

        data = {
            "store": store,
            "products": products
        }

        current_datetime = timezone.now()
        str_datetime = current_datetime.strftime("%d_%m_%Y_%H:%M:%S")

        return self.generate_pdf_report(f"product_list_{str_datetime}", "store/reports/product.html", data)
    

class DownloadSalesReport(LoginRequiredMixin, ReportingMixin, View):
    def get(self, request, *args, **kwargs):
        store = Store.objects.for_user_admin(self.request.user)
        order_items: QuerySet[OrderItem] = OrderItem.objects.filter(order__store=store)


        header = ["order_id", "product_name",
                  "product_rating", "product_price", "quantity",
                  "total_quantity_cost", "percent_of_total_order", "total_order_cost"]
        data = [
            (
                order_item.order.id,
                order_item.product.name,
                order_item.product.rating,
                f"${order_item.product.price}",
                order_item.quantity,
                f"${order_item.product.price * order_item.quantity}",
                f"{round(((order_item.product.price * order_item.quantity) / order_item.order.total_cost) * 100)}%",
                f"${order_item.order.total_cost}",
            )
            for order_item in order_items
        ]

        current_datetime = timezone.now()
        str_datetime = current_datetime.strftime("%d_%m_%Y_%H:%M:%S")

        return self.generate_csv_report(f"{store.name.lower()}_sales_report_{str_datetime}", header, data)
    

class DownloadSalesPDFReport(LoginRequiredMixin, ReportingMixin, View):
    def get(self, request, *args, **kwargs):
        store = Store.objects.for_user_admin(self.request.user)
        order_items: QuerySet[OrderItem] = OrderItem.objects.filter(order__store=store)

        order_data = []
        order_cost_map = {}
        for order_item in order_items:
            order_id = order_item.order.id
            total_quantity_cost = order_item.product.price * order_item.quantity
            if order_id not in order_cost_map:
                order_cost_map[order_id] = 0

            order_data.append({
                "order_id": order_id,
                "product_name": order_item.product.name,
                "product_rating": order_item.product.rating,
                "product_price": order_item.product.price,
                "quantity": order_item.quantity,
                "total_quantity_cost": total_quantity_cost,
                "percent_of_total_order": round((total_quantity_cost / order_item.order.total_cost) * 100),
                "order_cost": order_item.order.total_cost,
            })

        data = {
            "store": store,
            "order_item_data": order_data
        }

        current_datetime = timezone.now()
        str_datetime = current_datetime.strftime("%d_%m_%Y_%H:%M:%S")

        return self.generate_pdf_report(f"{store.name.lower()}_sales_report_{str_datetime}", "store/reports/sales.html", data)
