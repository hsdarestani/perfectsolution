from django.urls import path
from . import views
app_name="shop"
urlpatterns=[path("",views.home,name="home"),path("produkte/",views.product_list,name="product_list"),path("produkt/<slug:slug>/",views.product_detail,name="product_detail"),path("warenkorb/",views.cart_view,name="cart"),path("warenkorb/add/<int:product_id>/",views.cart_add,name="cart_add"),path("warenkorb/update/<int:product_id>/",views.cart_update,name="cart_update"),path("warenkorb/remove/<int:product_id>/",views.cart_remove,name="cart_remove"),path("checkout/",views.checkout,name="checkout"),path("bestellung/<str:number>/erfolgreich/",views.order_success,name="order_success"),path("geschaeftskonto/",views.business_account_request,name="business_account_request"),path("health/",views.health,name="health")]
