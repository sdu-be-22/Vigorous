from django.urls import URLPattern, path
from pip import main
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
    
]
