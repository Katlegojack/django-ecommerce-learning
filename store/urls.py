from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('products/',views.products, name='products'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('products/<int:id>/',views.product_detail,name='product_detail'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('reset-cart/', views.reset_cart, name='reset_cart'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('increase/<int:id>/', views.increase_qyt, name='increase'),
    path('decrease/<int:id>/', views.decrease_qyt, name='decrease'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.my_orders, name='my_orders'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),

]
