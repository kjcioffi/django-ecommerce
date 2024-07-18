from collections import defaultdict
from store.models import Order, OrderItem, Product, Store


def get_products_and_quantities_from_bag(request):
    products = []
    if "bag" in request.session:
        for product in request.session["bag"]:
            product_instance = Product.objects.get(id=product["product_id"])
            products.append(
                {
                    "product": product_instance,
                    "quantity": product["quantity"],
                    "image": product_instance.image.url,
                }
            )
        return products
    else:
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