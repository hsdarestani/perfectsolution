from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import uuid

class Category(models.Model):
    name=models.CharField("Name",max_length=120,unique=True)
    slug=models.SlugField("URL",max_length=140,unique=True,blank=True)
    sort_order=models.PositiveIntegerField("Sortierung",default=0)
    active=models.BooleanField("Aktiv",default=True)
    class Meta:
        ordering=("sort_order","name")
        verbose_name="Kategorie"
        verbose_name_plural="Kategorien"
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.name)
        super().save(*a,**kw)
    def __str__(self):return self.name

class Product(models.Model):
    UNITS=[("Stk","Stück"),("Pack","Packung"),("Ktn","Karton"),("L","Liter"),("kg","Kilogramm")]
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name="products",verbose_name="Kategorie")
    sku=models.CharField("Artikelnummer",max_length=80,unique=True)
    ean=models.CharField("EAN",max_length=32,blank=True)
    name=models.CharField("Produktname",max_length=220)
    slug=models.SlugField("URL",max_length=250,unique=True,blank=True)
    short_description=models.CharField("Kurzbeschreibung",max_length=300,blank=True)
    description=models.TextField("Beschreibung",blank=True)
    net_price=models.DecimalField("Nettopreis",max_digits=10,decimal_places=2,default=0)
    vat_rate=models.DecimalField("MwSt. %",max_digits=5,decimal_places=2,default=19)
    stock=models.IntegerField("Bestand",default=0)
    min_order_qty=models.PositiveIntegerField("Mindestmenge",default=1)
    unit=models.CharField("Einheit",max_length=12,choices=UNITS,default="Stk")
    image=models.FileField("Produktbild",upload_to="products/%Y/%m/",blank=True,null=True)
    active=models.BooleanField("Im Shop sichtbar",default=True)
    featured=models.BooleanField("Auf Startseite",default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=("name",)
        verbose_name="Produkt"
        verbose_name_plural="Produkte"
    def save(self,*a,**kw):
        if not self.slug:
            base=slugify(self.name)[:210] or self.sku.lower()
            candidate=base;n=2
            while Product.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate=f"{base}-{n}";n+=1
            self.slug=candidate
        super().save(*a,**kw)
    @property
    def gross_price(self):return (self.net_price*(Decimal("1")+self.vat_rate/Decimal("100"))).quantize(Decimal("0.01"))
    @property
    def stock_label(self):
        if self.stock<=0:return "Nicht auf Lager"
        if self.stock<=5:return "Wenig Bestand"
        return "Auf Lager"
    def get_absolute_url(self):return reverse("shop:product_detail",kwargs={"slug":self.slug})
    def __str__(self):return f"{self.sku} · {self.name}"

class BusinessAccountRequest(models.Model):
    STATUS=[("new","Neu"),("contacted","Kontaktiert"),("approved","Freigegeben"),("rejected","Abgelehnt")]
    company=models.CharField("Firma",max_length=200)
    name=models.CharField("Ansprechpartner",max_length=160)
    email=models.EmailField("E Mail")
    phone=models.CharField("Telefon",max_length=60,blank=True)
    vat_id=models.CharField("USt ID",max_length=50,blank=True)
    status=models.CharField("Status",max_length=20,choices=STATUS,default="new")
    created_at=models.DateTimeField("Eingang",auto_now_add=True)
    class Meta:
        ordering=("-created_at",)
        verbose_name="Geschäftskonto Anfrage"
        verbose_name_plural="Geschäftskonto Anfragen"
    def __str__(self):return self.company

class Order(models.Model):
    STATUS=[("new","Neu"),("confirmed","Bestätigt"),("processing","In Bearbeitung"),("shipped","Versendet"),("completed","Abgeschlossen"),("cancelled","Storniert")]
    PAY=[("pending","Offen"),("paid","Bezahlt"),("failed","Fehlgeschlagen"),("refunded","Erstattet")]
    METHODS=[("invoice","Rechnung"),("bank_transfer","Überweisung"),("online","Online Zahlung")]
    number=models.CharField("Bestellnummer",max_length=32,unique=True,editable=False)
    company=models.CharField("Firma",max_length=200,blank=True)
    customer_name=models.CharField("Name",max_length=160)
    email=models.EmailField("E Mail")
    phone=models.CharField("Telefon",max_length=60,blank=True)
    billing_address=models.TextField("Rechnungsadresse")
    shipping_address=models.TextField("Lieferadresse")
    status=models.CharField("Bestellstatus",max_length=20,choices=STATUS,default="new")
    payment_status=models.CharField("Zahlungsstatus",max_length=20,choices=PAY,default="pending")
    payment_method=models.CharField("Zahlungsart",max_length=30,choices=METHODS,default="invoice")
    net_total=models.DecimalField("Netto",max_digits=12,decimal_places=2,default=0)
    vat_total=models.DecimalField("MwSt.",max_digits=12,decimal_places=2,default=0)
    shipping_total=models.DecimalField("Versand",max_digits=12,decimal_places=2,default=0)
    gross_total=models.DecimalField("Gesamt",max_digits=12,decimal_places=2,default=0)
    customer_note=models.TextField("Kundenhinweis",blank=True)
    internal_note=models.TextField("Interne Notiz",blank=True)
    created_at=models.DateTimeField("Bestellt",auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=("-created_at",)
        verbose_name="Bestellung"
        verbose_name_plural="Bestellungen"
    def save(self,*a,**kw):
        if not self.number:self.number=f"PS-{timezone.now():%y%m%d}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*a,**kw)
    def __str__(self):return self.number

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    product_name=models.CharField(max_length=220)
    sku=models.CharField(max_length=80)
    quantity=models.PositiveIntegerField(default=1)
    unit_net_price=models.DecimalField(max_digits=10,decimal_places=2)
    vat_rate=models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self):return f"{self.quantity} × {self.product_name}"

class PaymentTransaction(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="payments")
    provider=models.CharField("Anbieter",max_length=60,blank=True)
    provider_reference=models.CharField("Referenz",max_length=160,blank=True)
    amount=models.DecimalField("Betrag",max_digits=12,decimal_places=2)
    status=models.CharField("Status",max_length=30,default="pending")
    payload=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):return f"{self.order.number} · {self.amount} €"
