from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import BusinessAccountRequestForm,CheckoutForm
from .models import Category,Order,OrderItem,Product
def base(request):return {"categories":Category.objects.filter(active=True),"cart_count":len(Cart(request))}
def home(request):
    c=base(request);p=Product.objects.filter(active=True);f=p.filter(featured=True)[:12];c.update({"products":f if f.exists() else p[:12],"account_form":BusinessAccountRequestForm()});return render(request,"shop/home.html",c)
def product_list(request):
    p=Product.objects.filter(active=True);q=request.GET.get("q","").strip();cat=request.GET.get("category","").strip()
    if q:p=p.filter(Q(name__icontains=q)|Q(sku__icontains=q)|Q(ean__icontains=q)|Q(description__icontains=q))
    if cat:p=p.filter(category__slug=cat)
    c=base(request);c.update({"products":p,"query":q,"active_category":cat});return render(request,"shop/product_list.html",c)
def product_detail(request,slug):
    c=base(request);c["product"]=get_object_or_404(Product,slug=slug,active=True);return render(request,"shop/product_detail.html",c)
@require_POST
def cart_add(request,product_id):
    p=get_object_or_404(Product,id=product_id,active=True)
    try:q=max(p.min_order_qty,int(request.POST.get("quantity",p.min_order_qty)))
    except:q=p.min_order_qty
    Cart(request).add(p,q);messages.success(request,"Produkt wurde hinzugefügt.");return redirect(request.POST.get("next") or "shop:cart")
@require_POST
def cart_update(request,product_id):
    p=get_object_or_404(Product,id=product_id,active=True)
    try:q=max(0,int(request.POST.get("quantity",1)))
    except:q=1
    Cart(request).add(p,q,True);return redirect("shop:cart")
@require_POST
def cart_remove(request,product_id):
    p=get_object_or_404(Product,id=product_id);Cart(request).remove(p);return redirect("shop:cart")
def cart_view(request):
    cart=Cart(request);c=base(request);c.update({"cart":list(cart),"totals":cart.totals()});return render(request,"shop/cart.html",c)
def business_account_request(request):
    form=BusinessAccountRequestForm(request.POST)
    if form.is_valid():form.save();messages.success(request,"Anfrage wurde gespeichert.")
    else:messages.error(request,"Bitte prüfen Sie die Angaben.")
    return redirect("shop:home")
def checkout(request):
    cart=Cart(request);items=list(cart)
    if not items:return redirect("shop:product_list")
    form=CheckoutForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        with transaction.atomic():
            d=form.cleaned_data;t=cart.totals();ship=d["billing_address"] if d["same_address"] else d["shipping_address"]
            o=Order.objects.create(company=d["company"],customer_name=d["customer_name"],email=d["email"],phone=d["phone"],billing_address=d["billing_address"],shipping_address=ship,payment_method=d["payment_method"],customer_note=d["customer_note"],net_total=t["net"],vat_total=t["vat"],gross_total=t["gross"])
            for i in items:
                p=Product.objects.select_for_update().get(pk=i["product"].pk)
                if p.stock>0:p.stock=max(0,p.stock-i["quantity"]);p.save(update_fields=["stock"])
                OrderItem.objects.create(order=o,product=p,product_name=p.name,sku=p.sku,quantity=i["quantity"],unit_net_price=p.net_price,vat_rate=p.vat_rate)
            cart.clear()
        return redirect("shop:order_success",number=o.number)
    c=base(request);c.update({"cart":items,"totals":cart.totals(),"form":form});return render(request,"shop/checkout.html",c)
def order_success(request,number):
    c=base(request);c["order"]=get_object_or_404(Order,number=number);return render(request,"shop/order_success.html",c)
def health(request):return JsonResponse({"ok":True})
