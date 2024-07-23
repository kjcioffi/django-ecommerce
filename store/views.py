from typing import Any
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from store.forms import OrderAdminForm, OrderForm, ProductAdminForm
from django.contrib.auth.decorators import login_required

from store.models import Order, Product, Store
from django.contrib.auth.mixins import LoginRequiredMixin

from store.view_utilities import create_orders_for_stores, get_order_items_by_store, get_products_and_quantities_from_bag


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
            create_orders_for_stores(stores, order_info)

            request.session["bag"] = []
            request.session["total_items"] = 0

            messages.add_message(
                request,
                messages.SUCCESS,
                "Order(s) placed! Thank you for your business, "
                "most customers recieve their orders in 2 - 3 business days. "
                "Please contact us if it has been more than 5 business days.",
            )

            return redirect("store:store_list")
    else:
        form = OrderForm()

    return render(
        request,
        "store/checkout.html",
        {"form": form, "products_in_bag": products_in_bag, "total_cost": total_cost},
    )


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
    template_name = "store/product_admin.html"
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

    return render(request, "store/product_admin_modify.html", {"form": form})


class ProductAdminAdd(LoginRequiredMixin, CreateView):
    form_class = ProductAdminForm
    template_name = "store/product_admin_add.html"
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
                    f"{order.name}({order.pk}) successfully saved.",
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
