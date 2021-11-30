from django.contrib import admin
from django.urls import path
from django.urls import path
from app1 import views
from eshop import settings
from django.conf.urls.static import static


urlpatterns = [
        path('',views.index,name="index"),
        path('index/',views.index,name="index"),
        path('buyer_register/',views.buyer_register,name="buyer_register"),
        path('seller_register/',views.seller_register,name="seller_register"),
        path("buyer_login/",views.buyer_login,name="buyer_login"),
        path("seller_login/",views.seller_login,name="seller_login"),
        path("customer_info/",views.customer_info,name="customer_info"),
        path("seller_info/",views.seller_info,name="seller_info"),
        path("good_info/<int:id>/",views.good_info,name="good_info"),
        path("logout/",views.logout,name="logout"),
        path("create_good/",views.create_good,name="create_good"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
