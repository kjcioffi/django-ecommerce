from collections import defaultdict
import csv

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from store.models import Order, OrderItem, Product, Store


class ReportingMixin:
    def generate_csv_report(self, filename, header, data):
        response: HttpResponse = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={filename}.csv"

        report = csv.writer(response)
        report.writerow(header)

        for row in data:
            report.writerow(row)

        return response
    
    def generate_pdf_report(self, filename, template_src, data, inline=True):
        response: HttpResponse = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"{'inline' if inline else 'attachment'}; filename={filename}.pdf"

        template = render_to_string(template_src, data)
        HTML(string=template).write_pdf(response)

        return response


def get_products_and_quantities_from_bag(request):
    products = []
    if "bag" in request.session:
        product_ids = [product["product_id"] for product in request.session["bag"]]
        product_instances = Product.objects.filter(id__in=product_ids)

        # Map model ids to model objects.
        product_dict = {product.id: product for product in product_instances}

        for product in request.session["bag"]:
            product_instance = product_dict.get(product["product_id"])
            if product_instance:
                products.append(
                    {
                        "product": product_instance,
                        "quantity": product["quantity"],
                        "image": product_instance.image.url,
                    }
                )
    return products


def get_order_items_by_store(products_in_bag):
    stores = defaultdict(list)

    for bag_item in products_in_bag:
        product: Product = bag_item["product"]

        product_store: Store = product.store

        # fetch order items based via store model object as dict key
        order_items_from_store: list = stores.get(product_store, [])

        # Add order item to store dict object.
        order_items_from_store.append(bag_item)

        # assign or overwrite dictionary key
        stores[product_store] = order_items_from_store

    return stores


def create_orders_for_stores(stores, order_info):
    for store in stores:
        bag_items: list = stores[store]
        order: Order = Order.objects.create(store=store, **order_info)

        for bag_item in bag_items:
            OrderItem.objects.create(
                order=order,
                product=bag_item["product"],
                quantity=bag_item["quantity"],
            )
