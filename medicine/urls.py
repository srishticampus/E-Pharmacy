from django.urls import path
from . import views
from django.urls import path
from .views import register_user, logout_view
from .views import product_list, product_detail, add_to_cart, cart



urlpatterns = [
    path('', views.index, name='index'),

    path('register/', register_user, name='register'),
    path('logout/', logout_view, name='logout'),


    # urls.py

    path('user_login_view', views.user_login_view, name='user_login'),
    path('doctor_login_view', views.doctor_login_view, name='doctor_login'),
    path('pharmacist_login_view', views.pharmacist_login_view, name='pharmacist_login'),


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

    path('register_doctor/', views.register_doctor, name='register_doctor'),
    path('register_pharmacist/', views.register_pharmacist, name='register_pharmacist'),
    path('register_admin/', views.register_admin, name='register_admin'),

    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('upload_prescription/', views.upload_prescription, name='upload_prescription'),
    path('view_prescriptions/', views.view_prescriptions, name='view_prescriptions'),
    path('prescription/success/', views.prescription_success, name='prescription_success'),
    path('all-doctors/', views.all_doctors, name='all_doctors'),
    path('status/', views.prescription_status, name='prescription_status'),
    path('my-prescriptions/', views.my_prescriptions, name='my_prescriptions'),
    path('pharmacist/dashboard/', views.pharmacist_dashboard, name='pharmacist_dashboard'),










    

]




