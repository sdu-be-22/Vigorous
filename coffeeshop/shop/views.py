from email import message
from itertools import product
from multiprocessing import context
from pkgutil import iter_importers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
import json
import datetime
from . forms import CommentForm, EmailForm
from .utils import cartData, cookieCart, guestOrder, sendEmail
from . forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    form = sendEmail(request)
    context = {
        'form':form,
        'title': 'Menu',
        'categories':categories,
        'products':products
    }
    return render(request, 'shop/shop.html', context = context )

def cart(request):
    data = cartData(request)

    order = data['order']
    items = data['items']
    form = sendEmail(request)
    context = {
        'form':form,
        'title': 'Cart',
        'items':items,
        'order': order 
    }
    return render(request, 'shop/cart.html', context )

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def checkout(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    form = sendEmail(request)
    context = {
        'form':form,
        'title': 'Checkout',
        'items':items,
        'order': order 
    }
    return render(request, 'shop/checkout.html', context )




def product_detail(request, slug):
    products = get_object_or_404(Product, slug = slug)
    eachProduct = Product.objects.get(slug=slug)
    form1 = CommentForm(instance=eachProduct)
    num_comments = Comment.objects.filter(product=eachProduct).count()



    if request.method == 'POST':
        form1 = CommentForm(request.POST,instance=eachProduct)
        if form1.is_valid():
            name = request.user.username
            body = form1.cleaned_data['comment_body']
            c = Comment(product=eachProduct, commenter_name=name, comment_body=body, date_added= datetime.datetime.now().timestamp())
            c.save()
            return redirect('shops:product_detail' ,slug)
        else:
            print('form is invalid')    
    else:
        form1 = CommentForm()    

    form = sendEmail(request)
    context = {
        'form':form,
        'product': products,
        'form1':form1,
        'eachProduct':eachProduct,
        'num_comments':num_comments,
    }
    return render(request, 'shop/detail.html', context)



def basic(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    form = sendEmail(request)
    context = {
        'form':form,
        'title': 'menu',
        'categories':categories,
        'products':products
    }
    return render(request, 'shop/basic.html',context)


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

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    
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

    print('Data:',request.body)
    return JsonResponse('Payment completed',safe=False)

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(name__contains=searched)
        return render(request, 'shop/search.html', {'searched':searched}, {'products':products})
    else:
        return render(request, 'shop/search.html')

from django.core.mail import send_mail
from django.conf import settings
def register(request):
    message = ''
    if request.method == "POST":
        form1 = UserRegisterForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            username = form1.cleaned_data.get('username')
            message = f'Hi {username}, your account was created successfully'
            send_mail('Account created', message,
                      settings.DEFAULT_FROM_EMAIL, [user.email])
            Customer.objects.create(user=user,name=user.username,email=user.email)
            return redirect('shops:login')
    else:
        form1 = UserRegisterForm()
    
    form = sendEmail(request)
    context = {
        'form':form,
        'form1':form1,
    }
    return render(request, 'shop/register.html', context)

@login_required()
def profile(request):
    return render(request, 'shop/profile.html')

