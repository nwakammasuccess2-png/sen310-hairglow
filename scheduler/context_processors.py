def cart_processor(request):
    cart = request.session.get('cart', {})
    count = 0
    for item in cart.values():
        try:
            count += int(item.get('quantity', 0))
        except (ValueError, TypeError):
            pass
    return {'cart_count': count}
