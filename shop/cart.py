from decimal import Decimal
from .models import Product
KEY="perfectsolution_cart"
class Cart:
    def __init__(self,request):self.session=request.session;self.cart=self.session.get(KEY,{})
    def add(self,p,quantity=1,override=False):
        k=str(p.id)
        if k not in self.cart:self.cart[k]={"quantity":0}
        self.cart[k]["quantity"]=quantity if override else self.cart[k]["quantity"]+quantity
        if self.cart[k]["quantity"]<=0:self.cart.pop(k,None)
        self.session[KEY]=self.cart;self.session.modified=True
    def remove(self,p):self.cart.pop(str(p.id),None);self.session[KEY]=self.cart;self.session.modified=True
    def clear(self):self.session.pop(KEY,None);self.cart={};self.session.modified=True
    def __len__(self):return sum(x["quantity"] for x in self.cart.values())
    def __iter__(self):
        for p in Product.objects.filter(id__in=self.cart.keys(),active=True):
            d=self.cart[str(p.id)].copy();d["product"]=p;d["net_total"]=p.net_price*d["quantity"];d["vat_total"]=d["net_total"]*p.vat_rate/Decimal("100");d["gross_total"]=d["net_total"]+d["vat_total"];yield d
    def totals(self):
        net=Decimal("0");vat=Decimal("0")
        for i in self:net+=i["net_total"];vat+=i["vat_total"]
        return {"net":net.quantize(Decimal(".01")),"vat":vat.quantize(Decimal(".01")),"gross":(net+vat).quantize(Decimal(".01"))}
