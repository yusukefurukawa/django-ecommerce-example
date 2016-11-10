import datetime
from django.shortcuts import redirect, render, get_list_or_404, render_to_response
from ecommerce.models import *

# Create your views here.

def set_cookie(response, key, value, max_age):
    """
    cookieに任意の情報をセットする場合に呼び出されるメソッドです。
    """

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

def index(request):
    """
    商品一覧画面(/ec/list/)が呼び出された際に呼び出されるビューです。
    商品情報を返します。
    """

    products = get_list_or_404(Product)

    response = render(request, 'product_list.html', {'products': products})

    return response

def cart_add(request, product_id):
    """
    カートに任意の商品を追加する場合に呼び出されるビューです。
    カート(cookie)に任意の商品の商品IDを追加します。
    """

    current_cart = list()   #   現在のカートを宣言します。
    #   カートの状態を調べて、カートの情報を取り出します。
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    #   current_cart(list)をcookieとして保存できる形式にするため文字列にします。
    current_cart_str = product_id
    if len(current_cart) > 0:
        #   listをカンマ区切りの文字列にします。
        for item in current_cart:
            current_cart_str = current_cart_str + ',' +  str(item)

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    set_cookie(response, 'cart', current_cart_str, 365*24*60*60)

    return response

def cart_delete(request, product_id):
    """
    カートに入っている任意の商品を削除する場合に呼び出されるビューです。
    カート(cookie)から任意の商品の商品IDを削除します。
    """

    current_cart = list()   #   現在のカートを宣言します。
    #   カートの状態を調べて、カートの情報を取り出します。
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    #   カートから当該のIDの商品を削除します。
    current_cart = [item for item in current_cart if item is not str(product_id)]

    #   current_cart(list)をcookieとして保存できる形式にするため文字列にします。
    current_cart_str = current_cart.pop()
    if len(current_cart) > 0:
        #   listをカンマ区切りの文字列にします。
        for item in current_cart:
            current_cart_str = current_cart_str + ',' +  str(item)

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    set_cookie(response, 'cart', current_cart_str, 365*24*60*60)

    return response


def cart_reset(request):
    """
    カートを空にするがクリックされた場合に実行されるビューです。
    カートの中身(cookie)を空にします。
    """

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    response.delete_cookie('cart')

    return response

def cart_list(request):
    """
    カートの中身を表示するページが表示される場合に実行されるビューです。
    カートに入っている商品情報を返します。
    """

    current_cart = list()   #   現在のカートを宣言します。
    #   カートの状態を調べて、カートの情報を取り出します。
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    #   カートに入っている商品の情報を取得します
    products = Product.objects.filter(id__in=current_cart)

    return render(request, 'cart_list.html', {'products': products})

def order(request):
    """
    注文画面が表示される場合に実行されるビューです。
    カートに入っている商品情報と決済方法と注文画面を返します。
    """

    current_cart = list()   #   現在のカートを宣言します。
    #   カートの状態を調べて、カートの情報を取り出します。
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    products = Product.objects.filter(id__in=current_cart)

    #   決済方法を取得します。
    payments = get_list_or_404(Payment)

    return render(request, 'order.html', {'products': products, 'payments': payments})

def order_execute(request):
    """
    注文画面からPOSTされた際に実行されるビューです。
    お客様情報を保存し注文された商品情報を保存します。
    """

    #   送信されたお客様情報を保存します。
    customer = Customer(first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        postal_code=request.POST['postal_code'],
                        prefecture=request.POST['prefecture'],
                        city=request.POST['city'],
                        street1=request.POST['street1'],
                        street2 =request.POST['street2'],
                        tel=request.POST['tel'],
                        email=request.POST['email'])
    customer.save()

    #   Paymentオブジェクトを取得します。
    payment = Payment.objects.get(id=int(request.POST['payment']))

    #   注文情報を保存します。
    order = Order(customer=customer, payment=payment)
    order.save()

    #   カートに入っている商品情報を取得し、注文された商品情報を保存します。
    current_cart = list()   #   現在のカートを宣言します。
    #   カートの状態を調べて、カートの情報を取り出します。
    if not request.COOKIES.get('cart') is None:
        current_cart = request.COOKIES.get('cart').split(',')

    products = Product.objects.filter(id__in=current_cart)

    for product in products:
        order_product = Order_Product(order=order, product=product, count=1, price=product.price)
        order_product.save()

    #   注文完了画面にリダイレクトします。
    return redirect('/ec/order_complete/')

def order_complete(request):
    """
    注文完了時に実行されるビューです。
    注文完了画面を返します。
    """

    return render_to_response('order_complete.html')
