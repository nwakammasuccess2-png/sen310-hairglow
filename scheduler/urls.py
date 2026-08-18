from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('book/check-availability/', views.check_availability, name='check_availability'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', views.order_success, name='order_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]