import json
import os
from tkinter.messagebox import NO
from django.shortcuts import redirect, render
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core import serializers
from urllib3 import HTTPResponse

from .models import Discount, Item, Order, Tax


stripe.api_key = os.environ.get('STRIPE_KEY_PUBL')


def checkout(request):
    return render(request, 'base/checkout.html')


def index(request):
    items = Item.objects.all()
    order_items = []
    print(request.session)

    order_id = request.session.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(pk=order_id)
            order_items = order.items.all()
        except Order.DoesNotExist:
            request.session['order_id'], order_id = None, None
            order = None
            pass
    else:
        order = None        
    try:
        discount = Discount.objects.get(pk=1)
    except Discount.DoesNotExist:
        discount = None

    try:
        tax = Tax.objects.get(pk=1)
    except Tax.DoesNotExist:
        tax = None

    context = {
        'items': items,
        'order': order,
        'order_items': order_items,
        'discount': discount,
        'tax': tax,
    }

    return render(request, 'base/index.html', context)


def add_to_order(request, item_id):
    create_order(request, item_id)
    orders = Order.objects.filter(pk=request.session['order_id'])
    items = Item.objects.filter(order__in=orders).distinct()
    order_list = [serializers.serialize('json', x) for x in [orders, items]]
    print(order_list)
    return JsonResponse(order_list, safe=False)


def create_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order, created = Order.objects.get_or_create(status='draft')
    order.save()
    order.items.add(item)
    order.save()
    order.save_total_price()
    request.session['order_id'] = order.id
    return order, item

# @require_POST
# def add_to_order(request, item_id):
#     item = get_object_or_404(Item, pk=item_id)
#     order, _ = Order.objects.get_or_create(pk=request.session.get('order_id'))
#     order.items.add(item)

#     order.save()

#     return JsonResponse({
#         'total_price': str(order.total_price),
#         'items': [{
#             'name': item.name,
#             'description': item.description,
#             'price': str(item.price),
#         } for item in order.items.all()],
#     })