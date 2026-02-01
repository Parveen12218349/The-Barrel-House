from django.urls import path
from . import views

urlpatterns = [
    path("place/", views.place_order, name="place_order"),  # For cart-based order
    path("place/<int:product_id>/", views.place_order_with_product, name="place_order_with_product"),  # For Buy Now
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path("history/", views.order_history, name="order_history"),

]
