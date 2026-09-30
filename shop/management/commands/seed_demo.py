from django.core.management.base import BaseCommand
from shop.models import Category,Product
CATS=["Reinigungsmittel","Hygiene und Papier","Tücher und Mopps","Müllentsorgung","Arbeitsschutz","Maschinen und Geräte","Spendersysteme","Reinigungswagen"]
DATA=[("PS-1001","Profi Allzweckreiniger","Reinigungsmittel","8.90",48),("PS-1002","Sanitärreiniger Daily","Reinigungsmittel","6.40",36),("PS-2001","Papierhandtücher Z Falzung","Hygiene und Papier","24.90",27),("PS-3001","Mikrofasertuch Universal","Tücher und Mopps","2.90",120),("PS-4001","Müllsäcke Extra Stark 120 L","Müllentsorgung","10.90",52),("PS-5001","Nitril Handschuhe 100 Stück","Arbeitsschutz","8.50",40),("PS-6001","Nass und Trockensauger Pro","Maschinen und Geräte","189.00",8),("PS-7001","Seifenspender Professional","Spendersysteme","29.90",22),("PS-8001","Reinigungswagen Compact","Reinigungswagen","159.00",6)]
class Command(BaseCommand):
    def handle(self,*a,**kw):
        cats={}
        for i,n in enumerate(CATS,1):cats[n],_=Category.objects.get_or_create(name=n,defaults={"sort_order":i*10})
        for sku,n,c,price,stock in DATA:Product.objects.get_or_create(sku=sku,defaults={"name":n,"category":cats[c],"net_price":price,"stock":stock,"featured":True})
        self.stdout.write("Demo Katalog bereit")
