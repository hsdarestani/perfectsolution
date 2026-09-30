from django.contrib import admin
from .models import Category,Product,Order,OrderItem,PaymentTransaction,BusinessAccountRequest
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=("name","sort_order","active");list_editable=("sort_order","active");search_fields=("name",)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name","sku","category","net_price","stock","unit","active","featured","updated_at")
    list_filter=("active","featured","category","unit")
    list_editable=("net_price","stock","active","featured")
    search_fields=("name","sku","ean","description")
    autocomplete_fields=("category",)
class OrderItemInline(admin.TabularInline):
    model=OrderItem;extra=0;readonly_fields=("product","product_name","sku","quantity","unit_net_price","vat_rate");can_delete=False
class PaymentInline(admin.TabularInline):
    model=PaymentTransaction;extra=0;readonly_fields=("created_at",)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("number","customer_name","company","gross_total","payment_method","payment_status","status","created_at")
    list_filter=("status","payment_status","payment_method","created_at")
    search_fields=("number","customer_name","company","email","phone")
    list_editable=("payment_status","status")
    inlines=(OrderItemInline,PaymentInline)
@admin.register(BusinessAccountRequest)
class BusinessAdmin(admin.ModelAdmin):
    list_display=("company","name","email","phone","status","created_at");list_editable=("status",);search_fields=("company","name","email")
@admin.register(PaymentTransaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display=("order","provider","amount","status","created_at")
