from django.urls import path
from . import views

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('dish/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('category/<int:category_id>/', views.dish_list, name='dish_by_category'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

]

