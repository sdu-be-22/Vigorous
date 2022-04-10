from itertools import product
from multiprocessing import context
from pkgutil import iter_importers
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
import json
import datetime
from . forms import CommentForm
# Create your views here.


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'title': 'Shop',
        'categories':categories,
        'products':products
    }
    return render(request, 'shop/shop.html', context = context )

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}


    context = {
        'title': 'Cart',
        'items':items,
        'order': order 
    }
    return render(request, 'shop/cart.html', context )

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}


    context = {
        'title': 'Checkout',
        'items':items,
        'order': order 
    }
    return render(request, 'shop/checkout.html', context )




def product_detail(request, slug):
    products = get_object_or_404(Product, slug = slug)
    eachProduct = Product.objects.get(slug=slug)
    form = CommentForm(instance=eachProduct)
    num_comments = Comment.objects.filter(product=eachProduct).count()



    if request.method == 'POST':
        form = CommentForm(request.POST,instance=eachProduct)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            c = Comment(product=eachProduct, commenter_name=name, comment_body=body, date_added= datetime.datetime.now().timestamp())
            c.save()
            return redirect('shops:product_detail' ,slug)
        else:
            print('form is invalid')    
    else:
        form = CommentForm()    


    context = {
        'product': products,
        'form':form,
        'eachProduct':eachProduct,
        'num_comments':num_comments,
    }
    return render(request, 'shop/detail.html', context)





def category_list(request, category_slug):
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category=category)

    context = {
        'category':category,
        'categories':categories,
        'products':products
    }
    return render(request, 'shop/category.html',)

def menu(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'title': 'menu',
        'categories':categories,
        'products':products
    }
    return render(request, 'shop/menu.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0


    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.order_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
                customer=customer,
                order = order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
            )
    else:
        print("User is not logged in")
    print('Data:',request.body)
    return JsonResponse('Payment completed',safe=False)

  