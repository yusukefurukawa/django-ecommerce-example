from ecommerce.models import Customer
from django.forms import ModelForm

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ["created_at", "updated_at"]
