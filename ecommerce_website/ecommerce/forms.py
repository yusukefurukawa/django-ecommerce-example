from ecommerce.models import Customer
from django.forms import ModelForm
from django import forms

class CustomerForm(ModelForm):
    postal_code = forms.CharField(label="郵便番号", widget=forms.TextInput(attrs={'class' : 'p-postal-code'}))
    prefecture = forms.CharField(label="都道府県", widget=forms.TextInput(attrs={'class' : 'p-region'}))
    city = forms.CharField(label="市区町村", widget=forms.TextInput(attrs={'class' : 'p-locality'}))
    street1 = forms.CharField(label="番地など", widget=forms.TextInput(attrs={'class' : 'p-street-address'}))
    street2 = forms.CharField(label="建物名など", widget=forms.TextInput(attrs={'class' : 'p-extended-address'}))
    class Meta:
        model = Customer
        exclude = ["created_at", "updated_at"]
