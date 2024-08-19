class StoreUtils:
    """
    Misc utilities for keeping logic out of models, views, forms, etc.
    """

    @staticmethod
    def generate_store_image_path(instance, filename):
        store_name = instance.name.replace(" ", "_").lower()
        return f"stores/{store_name}/{filename}"
