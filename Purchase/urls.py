from django.urls import path, include
from django.contrib.auth import views

from .views import add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, CheckoutView, PaymentView, final_checkout





urlpatterns = [
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('final-checkout/', final_checkout, name='f_checkout'),
    path('verify/<int:id>', PaymentView.as_view(), name='verify_payment'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),


]