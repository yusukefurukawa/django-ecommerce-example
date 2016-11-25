from ecommerce.models import Customer
from django.forms import ModelForm
from django import forms

class CustomerForm(ModelForm):
    first_name = forms.CharField(label="名", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name = forms.CharField(label="姓", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    postal_code = forms.CharField(label="郵便番号", widget=forms.TextInput(attrs={'class' : 'form-control p-postal-code'}))
    prefecture = forms.CharField(label="都道府県", widget=forms.TextInput(attrs={'class' : 'form-control p-region'}))
    city = forms.CharField(label="市区町村", widget=forms.TextInput(attrs={'class' : 'form-control p-locality'}))
    street1 = forms.CharField(label="番地など", widget=forms.TextInput(attrs={'class' : 'form-control p-street-address'}))
    street2 = forms.CharField(label="建物名など", widget=forms.TextInput(attrs={'class' : 'form-control p-extended-address'}))
    tel = forms.CharField(label="電話番号", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(label="メールアドレス", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = Customer
        exclude = ["created_at", "updated_at"]


class CountForm(forms.Form):
    STATUS_CHOICES = (
            (1, "1"),   
            (2, "2"),   
            (3, "3"),   
            (4, "4"),   
            (5, "5"))
    count = forms.ChoiceField(label="個数", choices=STATUS_CHOICES)
