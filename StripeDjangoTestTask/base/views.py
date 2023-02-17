from django.shortcuts import redirect, render
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Discount, Item, Order, Tax
import os


stripe.api_key = os.environ.get('STRIPE_KEY')


def checkout(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'base/checkout.html', {'order': order})


def calculate_order_amount(curr_order):
    order = curr_order
    return int(order.total_price * 100)


def create_payment_intent(request):
    order = Order.objects.get(pk=request.session['order_id'])
    if request.method == 'POST':
        try:
            intent = stripe.PaymentIntent.create(
                amount=calculate_order_amount(order),
                currency='usd'
            )
            return JsonResponse({'clientSecret': intent.client_secret})

        except Exception as e:
            return e


def index(request):
    items = Item.objects.all()
    order_id = request.session.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            request.session['order_id'], order_id = None, None
            order = None
            pass
    else:
        order = None
    try:
        discount = Discount.objects.all()
    except Discount.DoesNotExist:
        discount = None

    try:
        tax = Tax.objects.get(pk=1)
    except Tax.DoesNotExist:
        tax = None

    context = {
        'items': items,
        'order': order,
        'discount': discount,
        'tax': tax,
    }

    return render(request, 'base/index.html', context)


def add_to_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    tax = Tax.objects.get(pk=1)
    order, created = Order.objects.get_or_create(status='draft')
    order.save()
    order.tax = tax
    order.items.add(item)
    order.save()
    order.save_total_price()
    request.session['order_id'] = order.id
    return redirect('home')


def remove_from_order(request, item_id):
    item = Item.objects.get(pk=item_id)
    order = Order.objects.get(pk=request.session['order_id'])
    order.items.remove(item)
    order.save_total_price()
    return redirect('home')


def apply_discount(request, discount_id):
    order = Order.objects.get(pk=request.session['order_id'])
    discount = Discount.objects.get(pk=discount_id)
    order.discount = discount
    order.save()
    order.save_total_price()
    return redirect('home')
