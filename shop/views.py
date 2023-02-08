from django.shortcuts import render, redirect
from .models import Product, Order, ShippingAddress, User
from django.http import JsonResponse
import json
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout



def user_registration(request):
    """
        Function Name: user_registration
        Description: Signup to access the site
        Return: user info
    """
    if request.method == 'POST':

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return HttpResponseRedirect(request.path_info)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Taken')
                return HttpResponseRedirect(request.path_info)
            else:
                User.objects.create_user(
                    username=username, email=email, password=password)
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return HttpResponseRedirect(request.path_info)

    else:
        return render(request, 'shop/signup.html')


def login_view(request):
    """
        Function Name: login_view
        Description: login to access the site
        Return: user info
    """

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/shop')
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'shop/login.html')
    else:
        return render(request, 'shop/login.html')


def shop(request):
    """
        Function Name: shop
        Description: list of all items in the 
                    ecommerce app
        Return: list of all items
    """
    products = Product.objects.all()
    context={
        "products":products
        }
    return render(request, 'shop/shop.html', context)


def view_single_product(request, pk):
    """
        Function Name: view_single_product
        Description: to view single product detail
        Return: single product
    """
    product = Product.objects.get(id=pk)
    context = {
        "product":product
    }
    return render(request, 'shop/view_single_item.html', context)


def cart(request):
    """
        Function Name: cart
        Description: list of items that you wish to buy
        Return: cart data
    """
    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context={"items":items, "order":order}
    return render(request, 'shop/cart.html', context)


def checkout(request):
    """
        Function Name: checkout
        Description: checkout page to display the 
                    items that you are like to buy
        Return: checkout page details
    """
    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context={"items":items, "order":order}
    return render(request, 'shop/checkout.html', context)


def processorder(request):
    """
        Function Name: processorder
        Description: to process the order 
                and save the shipping details 
        Return: redirect to payment
    """
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            pincode=data['shipping']['pincode']
        )
    return JsonResponse("payment completed", safe=False)


def logout_view(request):
    """
        Function Name: logout_view
        Description: to logout from the site 
        Return: login page
    """
    logout(request)
    return redirect("/")