from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Category, Cart, CartItem, Order, OrderItem
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required

def dish_list(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(available=True)
    return render(request, 'menu/dish_list.html', {'categories': categories, 'dishes': dishes})

def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, 'menu/dish_detail.html', {'dish': dish})

def dish_list(request, category_id=None):
    categories = Category.objects.all()
    dishes = Dish.objects.all()
    selected_category = None

    query = request.GET.get('q')

    if query:
        dishes = dishes.filter(name__icontains=query)

    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        dishes = dishes.filter(category=selected_category)

    context = {
        'categories': categories,
        'dishes': dishes,
        'selected_category': selected_category,
    }
    return render(request, 'menu/dish_list.html', context)

@receiver(post_save, sender=CustomUser)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)



@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.user.cart

    item = CartItem.objects.filter(cart=cart, dish=dish).first()

    if item:
        item.quantity += 1
        item.save()
    else:
        CartItem.objects.create(cart=cart, dish=dish, quantity=1)

    return redirect('dish_detail', pk=dish.id)


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')


@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'menu/cart.html', {'cart': cart})


from .forms import OrderForm
from .models import CartItem, Order, OrderItem

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        return redirect('view_cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    dish=item.dish,
                    quantity=item.quantity,
                    price=item.dish.price,
                )
            cart.items.all().delete()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'menu/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'menu/order_confirmation.html', {'order': order})
