from straw_catalog.models import Cart, Order, OrderItem, CartItem, Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

@login_required
def place_order(request):
    cart = get_cart_for_user(request)
    if not cart.items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('view_cart')

    order = Order.objects.create(user=request.user)
    for item in cart.items.all():
        OrderItem.objects.create(order=order, dish=item, quantity=1)

    cart.items.clear()
    messages.success(request, "Замовлення успішно оформлено.")
    return redirect('orders:order_history')

def get_cart_for_user(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def repeat_order(request, order_id):
    original_order = get_object_or_404(Order, id=order_id, user=request.user)


    cart, created = Cart.objects.get_or_create(user=request.user)


    for item in original_order.items.all():
        CartItem.objects.create(cart=cart, dish=item.dish, quantity=item.quantity)

    return redirect('view_cart')