# Generated for Perfect Solution production schema
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessAccountRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company", models.CharField(max_length=200, verbose_name="Firma")),
                ("name", models.CharField(max_length=160, verbose_name="Ansprechpartner")),
                ("email", models.EmailField(max_length=254, verbose_name="E Mail")),
                ("phone", models.CharField(blank=True, max_length=60, verbose_name="Telefon")),
                ("vat_id", models.CharField(blank=True, max_length=50, verbose_name="USt ID")),
                ("status", models.CharField(choices=[("new","Neu"),("contacted","Kontaktiert"),("approved","Freigegeben"),("rejected","Abgelehnt")], default="new", max_length=20, verbose_name="Status")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Eingang")),
            ],
            options={"verbose_name":"Geschäftskonto Anfrage","verbose_name_plural":"Geschäftskonto Anfragen","ordering":("-created_at",)},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="Name")),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True, verbose_name="URL")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Sortierung")),
                ("active", models.BooleanField(default=True, verbose_name="Aktiv")),
            ],
            options={"verbose_name":"Kategorie","verbose_name_plural":"Kategorien","ordering":("sort_order","name")},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(editable=False, max_length=32, unique=True, verbose_name="Bestellnummer")),
                ("company", models.CharField(blank=True, max_length=200, verbose_name="Firma")),
                ("customer_name", models.CharField(max_length=160, verbose_name="Name")),
                ("email", models.EmailField(max_length=254, verbose_name="E Mail")),
                ("phone", models.CharField(blank=True, max_length=60, verbose_name="Telefon")),
                ("billing_address", models.TextField(verbose_name="Rechnungsadresse")),
                ("shipping_address", models.TextField(verbose_name="Lieferadresse")),
                ("status", models.CharField(choices=[("new","Neu"),("confirmed","Bestätigt"),("processing","In Bearbeitung"),("shipped","Versendet"),("completed","Abgeschlossen"),("cancelled","Storniert")], default="new", max_length=20, verbose_name="Bestellstatus")),
                ("payment_status", models.CharField(choices=[("pending","Offen"),("paid","Bezahlt"),("failed","Fehlgeschlagen"),("refunded","Erstattet")], default="pending", max_length=20, verbose_name="Zahlungsstatus")),
                ("payment_method", models.CharField(choices=[("invoice","Rechnung"),("bank_transfer","Überweisung"),("online","Online Zahlung")], default="invoice", max_length=30, verbose_name="Zahlungsart")),
                ("net_total", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Netto")),
                ("vat_total", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="MwSt.")),
                ("shipping_total", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Versand")),
                ("gross_total", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Gesamt")),
                ("customer_note", models.TextField(blank=True, verbose_name="Kundenhinweis")),
                ("internal_note", models.TextField(blank=True, verbose_name="Interne Notiz")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Bestellt")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name":"Bestellung","verbose_name_plural":"Bestellungen","ordering":("-created_at",)},
        ),
        migrations.CreateModel(
            name="PaymentTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.CharField(blank=True, max_length=60, verbose_name="Anbieter")),
                ("provider_reference", models.CharField(blank=True, max_length=160, verbose_name="Referenz")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Betrag")),
                ("status", models.CharField(default="pending", max_length=30, verbose_name="Status")),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="shop.order")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sku", models.CharField(max_length=80, unique=True, verbose_name="Artikelnummer")),
                ("ean", models.CharField(blank=True, max_length=32, verbose_name="EAN")),
                ("name", models.CharField(max_length=220, verbose_name="Produktname")),
                ("slug", models.SlugField(blank=True, max_length=250, unique=True, verbose_name="URL")),
                ("short_description", models.CharField(blank=True, max_length=300, verbose_name="Kurzbeschreibung")),
                ("description", models.TextField(blank=True, verbose_name="Beschreibung")),
                ("net_price", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Nettopreis")),
                ("vat_rate", models.DecimalField(decimal_places=2, default=19, max_digits=5, verbose_name="MwSt. %")),
                ("stock", models.IntegerField(default=0, verbose_name="Bestand")),
                ("min_order_qty", models.PositiveIntegerField(default=1, verbose_name="Mindestmenge")),
                ("unit", models.CharField(choices=[("Stk","Stück"),("Pack","Packung"),("Ktn","Karton"),("L","Liter"),("kg","Kilogramm")], default="Stk", max_length=12, verbose_name="Einheit")),
                ("image", models.FileField(blank=True, null=True, upload_to="products/%Y/%m/", verbose_name="Produktbild")),
                ("active", models.BooleanField(default=True, verbose_name="Im Shop sichtbar")),
                ("featured", models.BooleanField(default=False, verbose_name="Auf Startseite")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="shop.category", verbose_name="Kategorie")),
            ],
            options={"verbose_name":"Produkt","verbose_name_plural":"Produkte","ordering":("name",)},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=220)),
                ("sku", models.CharField(max_length=80)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("unit_net_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("vat_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="shop.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="shop.product")),
            ],
        ),
    ]
