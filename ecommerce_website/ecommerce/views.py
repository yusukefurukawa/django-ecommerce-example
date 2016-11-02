from django.shortcuts import render, get_list_or_404
from ecommerce.models import Product

# Create your views here.

def index(request):
    products = get_list_or_404(Product)
    return render(request, 'product_list.html', {'products': products})
