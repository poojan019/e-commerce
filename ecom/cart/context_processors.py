from .cart import Cart

# Context processor so cart can work on all pages
def cart(request):
    return {'cart': Cart(request)}