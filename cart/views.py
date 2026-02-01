from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('view_cart')
    return redirect('products')  # fallback in case of GET


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # Check if any item is out of stock
    out_of_stock = any(item.quantity > item.product.stock for item in cart_items)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'out_of_stock': out_of_stock,
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def proceed_to_checkout(request):
    return redirect('place_order')  # This connects cart to your existing order placement view
