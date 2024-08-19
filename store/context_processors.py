def bag_items_processor(request):
    total_items = request.session.get("total_items", 0)
    return {"total_items": total_items}
