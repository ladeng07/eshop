from django.contrib import admin
from django.urls import path
from django.urls import path
from app1 import views


urlpatterns = [
        path('',views.index,name="index"),
        path('index/',views.index,name="index"),
        path('buyer_register/',views.buyer_register,name="buyer_register"),
        path('seller_register/',views.seller_register,name="seller_register"),
        path("buyer_login/",views.buyer_login,name="buyer_login"),
        path("seller_login/",views.seller_login,name="seller_login"),
]
