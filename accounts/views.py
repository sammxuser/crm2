from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
# Create your views here.

def home(request):
    total_orders = Order.objects.all().count()
    delivered_orders = Order.objects.all().filter(status='Delivered').count()
    pending_orders = Order.objects.all().filter(status='Pending').count()
    out_for_delivery_orders = Order.objects.all().filter(status='Out for delivery').count()

    customers = Customer.objects.all()
    last_five_orders = Order.objects.all().order_by('-date_created')[:5]

    context = {'total_orders': total_orders,
               'delivered_orders':delivered_orders,
               'pending_orders': pending_orders,
               'out_for_delivery_orders':out_for_delivery_orders,

               'customers': customers,
               'last_five_orders': last_five_orders

      }
    return render(request,'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'accounts/products.html',context)

def customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer_orders = Order.objects.filter(customer=customer)
    total_customer_orders = customer_orders.count()
    customer_pending_orders = customer_orders.filter(status='Pending').count()
    customer_delivered_orders = customer_orders.filter(status='Delivered').count()
    customer_enroute_orders = customer_orders.filter(status='Out for delivery').count()
    context = {
        'customer':customer,
        'customer_orders':customer_orders,
        'total_customer_orders': total_customer_orders,
        'customer_pending_orders': customer_pending_orders,
        'customer_delivered_orders': customer_delivered_orders,
        'customer_enroute_orders': customer_enroute_orders
    }
    
    return render(request, 'accounts/customerprofile.html', context)

def createOrder(request):
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if  form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}

    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    item = Order.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
        
    context = { 'item': item}
    return render(request, 'accounts/delete_order.html', context)