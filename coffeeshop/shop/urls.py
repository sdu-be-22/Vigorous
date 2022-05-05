from django.urls import URLPattern, path
from pip import main
from django.contrib.auth import views as auth_view
from . import views

app_name = 'shops'

urlpatterns = [
    path('',views.base, name='base'),
    path('cart/',views.cart, name="cart"),
    path('checkout/', views.checkout,name="checkout"),
    path('menu/',views.shop,name='shop'),

    path('update_item/', views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name='process_order'),
    
    path('product/<slug:slug>/',views.product_detail,name="product_detail"),
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='shop/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='shop/logout.html'), name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="shop/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="shop/password_reset_done.html"), name="password_reset_complete"),
]
