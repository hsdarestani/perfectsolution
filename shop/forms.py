from django import forms
from .models import BusinessAccountRequest
class BusinessAccountRequestForm(forms.ModelForm):
    consent=forms.BooleanField(required=True)
    class Meta:
        model=BusinessAccountRequest
        fields=("company","name","email","phone","vat_id")
class CheckoutForm(forms.Form):
    company=forms.CharField(required=False,max_length=200)
    customer_name=forms.CharField(max_length=160)
    email=forms.EmailField()
    phone=forms.CharField(required=False,max_length=60)
    billing_address=forms.CharField(widget=forms.Textarea(attrs={"rows":4}))
    same_address=forms.BooleanField(required=False,initial=True)
    shipping_address=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":4}))
    payment_method=forms.ChoiceField(choices=[("invoice","Rechnung"),("bank_transfer","Überweisung")])
    customer_note=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":3}))
    consent=forms.BooleanField(required=True)
