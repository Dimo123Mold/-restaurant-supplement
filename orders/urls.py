from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.order_history, name='order_history'),
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('place/', views.place_order, name='place_order'),
]
