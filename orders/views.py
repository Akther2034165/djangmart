from django.shortcuts import render,redirect
from cart.models import Cart,CartItem
from . forms import OrderForm
from . models import Order
import datetime


# Create your views here.
def place_order(request,total=0,quantity=0):
    current_user = request.user
    # if cart count is less than 0 then redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = tax + total
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = current_user
            form.instance.order_total = grand_total
            form.instance.tax = tax
            form.instance.ip = request.META.get('REMOTE_ADDR')
            saved_instance = form.save()
            saved_instance_id = saved_instance.id
            # generate order nummber
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date+saved_instance_id
            form.instance.order_number = order_number
            form.save()
            
            return redirect('checkout')
    else:
        return redirect('checkout')