import imp
from django.contrib import admin
from .models import *


admin.site.register((Item, Order, Discount, Tax,))
