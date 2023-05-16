from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrdeForm
from .models import Order
import datetime
from .models import Order, Payment, OrderProduct
from store.models import Product

# Create your views here.

def payments(request):
  

  return render(request, 'orderss/payments.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    total= 0
    quantity = 0
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    grand_total = total

    if request.method == 'POST':
        form = OrdeForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.addres_line_1 = form.cleaned_data['addres_line_1']
            data.addres_line_2 = form.cleaned_data['addres_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr=int(datetime.date.today().strftime('%Y'))
            mt=int(datetime.date.today().strftime('%m'))
            dt=int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                 'order':order,
                 'cart_items': cart_items,
                 'total':total,
                 'grand_total':grand_total,
            }

            for item in cart_items:
                orderproduct = OrderProduct()
                

                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

                CartItem.objects.filter(user=request.user).delete()


            return render(request, 'store/checkout.html', context)
    else:
            return redirect('checkout')
			
			
