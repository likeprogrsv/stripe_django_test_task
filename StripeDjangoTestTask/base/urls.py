from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('checkout/<int:order_id>', views.checkout, name='checkout'),

    path('checkout/create-payment-intent', views.create_payment_intent,
         name='create-payment-intent'),

    path('add-to-order/<int:item_id>/', views.add_to_order,
         name='add-to-order'),

    path('remove-from-order/<int:item_id>/', views.remove_from_order,
         name='remove-from-order'),

    path('apply-discount/<int:discount_id>/', views.apply_discount,
         name='apply-discount'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
