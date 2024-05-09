from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.vendor_detail),
    path('vendors/<int:vendor_id>/', views.vendor_detail),
    path('purchase_orders/', views.create_purchase_order),
    path('purchase_orders/<int:po_id>/', views.create_purchase_order),
    path('vendors/<int:vendor_id>/performance/', views.get_vendor_performance),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order),
]
