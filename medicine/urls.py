from django.urls import path
from . import views
from django.urls import path
from .views import register_user, login_view, logout_view
from .views import product_list, product_detail, add_to_cart, cart



urlpatterns = [
    path('', views.index, name='index'),

    path('register/', register_user, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:item_index>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),


    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('product/<int:product_id>/buy/', views.purchase_product, name='purchase_product'),
    path('purchase-confirmation/<int:product_id>/', views.purchase_confirmation, name='purchase_confirmation'),
    path('payment-success/', views.payment_success_view, name='payment_success'),

]




