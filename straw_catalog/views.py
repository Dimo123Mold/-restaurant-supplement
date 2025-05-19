from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Category, Cart, CartItem
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

    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        dishes = dishes.filter(category=selected_category)
    else:
        selected_category = None

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
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)

    if not created:
        item.quantity += 1
    item.save()
    return redirect('view_cart')


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