import datetime
from django.shortcuts import redirect, render, get_list_or_404, render_to_response
from ecommerce.models import Product

# Create your views here.

def set_cookie(response, key, value, max_age):
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

def index(request):
    products = get_list_or_404(Product)
    response = render(request, 'product_list.html', {'products': products})
    return response

def cart_add(request, product_id):
    current_cart = list()   #   現在のカート(Python内部ではlist)を宣言する
    #   カートの状態を調べて、カートの情報を取り出します
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    #   current_cart(list)を cookieとして保存できる形式にするためstrにします
    current_cart_str = product_id
    if len(current_cart) > 0:
        #   list をカンマ区切りのstrにする処理
        for item in current_cart:
            current_cart_str = current_cart_str + ',' +  str(item)

    products = get_list_or_404(Product)
    response = redirect('/ec/list/', {'products': products})
    set_cookie(response, 'cart', current_cart_str, 365*24*60*60)
    return response

def cart_delete(request, product_id):
    current_cart = list()   #   現在のカート(Python内部ではlist)を宣言する
    #   カートの状態を調べて、カートの情報を取り出します
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    #   カートから当該のIDの商品を消します
    current_cart = [item for item in current_cart if item is not str(product_id)]

    #   current_cart(list)を cookieとして保存できる形式にするためstrにします
    current_cart_str = current_cart.pop()
    if len(current_cart) > 0:
        #   list をカンマ区切りのstrにする処理
        for item in current_cart:
            current_cart_str = current_cart_str + ',' +  str(item)

    products = get_list_or_404(Product)
    response = redirect('/ec/list/', {'products': products})
    set_cookie(response, 'cart', current_cart_str, 365*24*60*60)
    return response


def cart_reset(request):
    products = get_list_or_404(Product)
    response = redirect('/ec/list/', {'products': products})
    response.delete_cookie('cart')
    return response

def cart_list(request):
    current_cart = list()   #   現在のカート(Python内部ではlist)を宣言する
    #   カートの状態を調べて、カートの情報を取り出します
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    #   カートに入っている商品の情報を取得します
    products = Product.objects.filter(id__in=current_cart)
    return render(request, 'cart_list.html', {'products': products})
