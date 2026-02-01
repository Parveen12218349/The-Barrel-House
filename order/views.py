from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from products.models import Product

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        mobile_number = request.POST.get('mobile_number')

        shipping_address = f"{street}, {city}, {state}, {postal_code}, {country}. Mobile: {mobile_number}"

        payment_method = request.POST.get('payment_method')

        if cart_items.exists():
            order = Order.objects.create(
                buyer=request.user,
                shipping_address=shipping_address,
                payment_method=payment_method,
                total_amount=total_price
            )

            # Check stock before placing order
            for item in cart_items:
                if item.quantity > item.product.stock:
                    return redirect('cart')  # or use Django messages to show 'Out of stock'

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                item.product.stock -= item.quantity
                item.product.save()

            cart_items.delete()
            return redirect('order_success', order_id=order.id)
        else:
            return redirect('place_order')  # cart empty fallback

    return render(request, 'orders/place_order.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
@login_required
def place_order_with_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    total_price = product.price

    if request.method == 'POST':
        if product.stock < 1:
            # Prevent ordering if out of stock
            return redirect('dashboard')

        # Collect shipping & payment data
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        mobile_number = request.POST.get('mobile_number')
        shipping_address = f"{street}, {city}, {state}, {postal_code}, {country}. Mobile: {mobile_number}"
        payment_method = request.POST.get('payment_method')

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method,
            total_amount=total_price
        )

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

        # Decrease product stock after order is confirmed
        product.stock -= 1
        product.save()

        return redirect('order_success', order_id=order.id)

    return render(request, 'orders/place_order.html', {
        'single_product': product,
        'total_price': total_price
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    order_items = OrderItem.objects.filter(order=order)

    # Check if it's a single product order
    if order_items.count() == 1 and order_items[0].quantity == 1:
        single_product = order_items[0].product
    else:
        single_product = None

    return render(request, 'orders/order_success.html', {
        'order': order,
        'single_product': single_product,
        'order_items': order_items if not single_product else None,
        'total_price': order.total_amount,
        'shipping_address': order.shipping_address,
        'payment_method': order.payment_method,
    })


# Order history view
def order_history(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {
        'orders': orders
    })

