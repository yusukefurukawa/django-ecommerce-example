import datetime
from django.shortcuts import redirect, render, get_list_or_404, render_to_response
from ecommerce.models import *
from ecommerce.forms import CustomerForm
from django.forms import modelformset_factory
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
    
    #if hasattr(request, "session") and request.session.get('cart', "None"):
    #    current_cart = request.session.get('cart').split(',')
    
    #   current_cart(list)をcookieとして保存できる形式にするため文字列にします。
    current_cart_str = product_id
    if len(current_cart) > 0:
        #   listをカンマ区切りの文字列にします。
        for item in current_cart:
            current_cart_str = current_cart_str + ',' +  str(item)

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    
    if not "new_cart" in request.session:
        request.session["new_cart"] = {}
    if product_id in request.session["new_cart"].keys():
        request.session["new_cart"][product_id]["order_count"] += 1
    else:
        request.session["new_cart"][product_id] = {}
        request.session["new_cart"][product_id]["order_count"] = 1
        request.session["new_cart"][product_id]["name"] = Product.objects.get(pk=product_id).name
        request.session["new_cart"][product_id]["id"] = Product.objects.get(pk=product_id).id
        request.session["new_cart"][product_id]["price"] = Product.objects.get(pk=product_id).price

    request.session.save() 
    print (request.session["new_cart"])
    
    request.session['cart'] = current_cart_str
    return response

def cart_delete(request, product_id):
    """
    カートに入っている任意の商品を削除する場合に呼び出されるビューです。
    カート(cookie)から任意の商品の商品IDを削除します。
    """
    print ("cart_delete{}".format(request.session["new_cart"]))
    if not "new_cart" in request.session:
        request.session["new_cart"] = {}
    if product_id in request.session["new_cart"].keys():
        request.session["new_cart"][product_id]["order_count"] -= 1
        print (request.session["new_cart"][product_id])
        if request.session["new_cart"][product_id]["order_count"] <= 0:
            del request.session["new_cart"][product_id]
    request.session.save() 
    print (request.session["new_cart"])
    products = get_list_or_404(Product)

    response = redirect('/ec/cart_list/', {'products': products})

    return response
        

def cart_reset(request):
    """
    カートを空にするがクリックされた場合に実行されるビューです。
    カートの中身(cookie)を空にします。
    """

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    request.session.flush()
    return response

def cart_list(request):
    """
    カートの中身を表示するページが表示される場合に実行されるビューです。
    カートに入っている商品情報を返します。
    """

    #current_cart = list()   #   現在のカートを宣言します。
    #   カートの状態を調べて、カートの情報を取り出します。
    cart = {}
    if hasattr(request, "session") and 'new_cart' in request.session:
        cart = request.session["new_cart"]
        print ("cart_list {}".format(cart))
    #   カートに入っている商品の情報を取得します
    return render(request, 'cart_list.html', {'products': cart})

def order(request):
    """
    注文画面が表示される場合に実行されるビューです。
    カートに入っている商品情報と決済方法と注文画面を返します。
    """
    if 'new_cart' in request.session:
        order_list = request.session["new_cart"]
    order_list = {}
    if not order_list:
        return render(request, 'error.html', {'error_message': "注文が空です"})

    #   カートの状態を調べて、カートの情報を取り出します。
    current_cart = request.session.get('new_cart')
    if not current_cart:
        current_cart = []
    products = Product.objects.filter(id__in=current_cart)

    order_list = []

    for product in products:
        order_list.append({"id": product.id,
                           "name": product.name,
                           "price": product.price,
                           "order_count": request.session["new_cart"][str(product.id)]["order_count"]
                                  })

    # 決済方法を取得します。
    payments = get_list_or_404(Payment)

    return render(request, 'order.html', {'form': CustomerForm(), 'products': order_list, 'payments': payments})

def order_execute(request):
    """
    注文画面からPOSTされた際に実行されるビューです。
    お客様情報を保存し注文された商品情報を保存します。
    """
    order_list = request.session["new_cart"]
    if request.method == "POST": 
        form = CustomerForm(request.POST)
        if form.is_valid():
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
            if not request.session.get('cart') is None:
                current_cart = request.session.get('cart').split(',')

            products = Product.objects.filter(id__in=current_cart)
            
                
            for key, product in order_list.items():
                order_product = Order_Product(order=order,
                                              product_id=int(product["id"]),
                                              count=product["order_count"], 
                                              price=product["price"])
                order_product.save()
            #   注文完了画面にリダイレクトします。
            return redirect('/ec/order_complete/')
    else:
        form = CustomerForm()
    return render(request, 'order.html', {'form': form, 'products': 'products', 'payments': 'payments'})

def order_complete(request):
    """
    注文完了時に実行されるビューです。
    注文完了画面を返します。
    """

    response = render_to_response('order_complete.html')

    #   カートの中身を削除します
    #response.delete_cookie('cart')
    request.session.flush()
    return response
