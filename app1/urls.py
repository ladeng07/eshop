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
        path('cart/',views.cart,name="cart"),
        path('address/',views.address,name="address"),
        path('order/',views.order,name="order"),
        path('order_info/',views.order_info,name="order_info"),
        path('edit_password/',views.edit_password,name="edit_password"),
        path('deal_order/',views.deal_order,name="deal_order"),
        path('reject_order/',views.reject_order,name="reject_order"),
        path('comment/',views.comment,name="comment"),
        path('delete_comment/',views.delete_comment,name="delete_comment"),
        path('deal_comment/',views.deal_comment,name="deal_comment"),
        path('deal_good/',views.deal_good,name="deal_good"),
        path('search/',views.search,name="search"),
        path('delete_good/',views.delete_good,name="delete_good"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
