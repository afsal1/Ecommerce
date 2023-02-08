from django.urls import path
from . import views

urlpatterns = [
    path('user_registration', views.user_registration, name="user_registration"),
    path('', views.login_view, name="login_view"),
    path('shop', views.shop, name="shop"),
    path('view_single_product/<str:pk>', views.view_single_product, name="view_single_product"),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('process_order', views.processorder, name="process_order"),
    path('logout', views.logout_view, name="logout"),
]

