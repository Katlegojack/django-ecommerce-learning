def cart_item_count(request):
    cart = request.session.get('cart', {})
    
    # Handle both cases - list or dict
    if isinstance(cart, dict):
        # If it's a dictionary, sum the values
        count = sum(cart.values())
    elif isinstance(cart, list):
        # If it's a list, count the items
        count = len(cart)
    else:
        # If it's neither, set to 0
        count = 0
    
    return {
        'cart_count': count
    }