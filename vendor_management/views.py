from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from .performance_logic import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, calculate_fulfillment_rate
from django.utils import timezone

@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    performance_data = {
        'on_time_delivery_rate': calculate_on_time_delivery_rate(vendor_id),
        'quality_rating_avg': calculate_quality_rating_avg(vendor_id),
        'average_response_time': calculate_average_response_time(vendor_id),
        'fulfillment_rate': calculate_fulfillment_rate(vendor_id)
    }
    
    serializer = VendorPerformanceSerializer(data=performance_data)
    serializer.is_valid()
    return Response(serializer.data)

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        # Retrieve the Purchase Order
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        
        # Update the Acknowledgment Date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        
        # Recalculate Average Response Time
        calculate_average_response_time(purchase_order.vendor_id)
        
        return Response({'message': 'Purchase order acknowledged successfully'}, status=status.HTTP_200_OK)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id=None):
    if request.method == 'GET':
        if vendor_id is not None:
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        try:
            serializer = VendorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Vendor created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorSerializer(vendor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            vendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def create_purchase_order(request, po_id=None):
    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Purchase order created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        if po_id is not None:
            try:
                purchase_order = PurchaseOrder.objects.get(pk=po_id)
                serializer = PurchaseOrderSerializer(purchase_order)
                return Response(serializer.data)
            except PurchaseOrder.DoesNotExist:
                return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data)

    elif request.method == 'PUT':
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.delete()
            return Response({'message': 'Purchase order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def get_vendor_performance(request, vendor_id):
#     try:
#         vendor = Vendor.objects.get(id=vendor_id)
#     except Vendor.DoesNotExist:
#         return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     performance_metrics = {
#         'on_time_delivery_rate': vendor.on_time_delivery_rate,
#         'quality_rating_avg': vendor.quality_rating_avg,
#         'average_response_time': vendor.average_response_time,
#         'fulfillment_rate': vendor.fulfillment_rate
#     }
#     return Response(performance_metrics)






# from django.http import JsonResponse
# from .models import Vendor,PurchaseOrder
# from django.views.decorators.csrf import csrf_exempt

# import json
# from django.http import JsonResponse

# @csrf_exempt
# def create_vendor(request):
#     if request.method == 'POST':
#         # Extract data from request body
#         try:
#             data = json.loads(request.body)
#             name = data.get('name')
#             contact_details = data.get('contact_details')
#             address = data.get('address')
#             vendor_code = data.get('vendor_code')

#             # Create new vendor instance
#             vendor = Vendor.objects.create(
#                 name=name,
#                 contact_details=contact_details,
#                 address=address,
#                 vendor_code=vendor_code
#             )
#             return JsonResponse({'message': 'Vendor created successfully'}, status=201)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


# @csrf_exempt
# def create_purchase_order(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON data from request body
#             data = json.loads(request.body)
            
#             # Extract data from JSON
#             po_number = data.get('po_number')
#             vendor_id = data.get('vendor_id')
#             order_date = data.get('order_date')
#             delivery_date = data.get('delivery_date')
#             items = data.get('items')
#             quantity = data.get('quantity')
#             status = data.get('status')
#             quality_rating = data.get('quality_rating')
#             issue_date = data.get('issue_date')
#             acknowledgment_date = data.get('acknowledgment_date')
            
#             # Create new purchase order
#             purchase_order = PurchaseOrder.objects.create(
#                 po_number=po_number,
#                 vendor_id=vendor_id,
#                 order_date=order_date,
#                 delivery_date=delivery_date,
#                 items=items,
#                 quantity=quantity,
#                 status=status,
#                 quality_rating=quality_rating,
#                 issue_date=issue_date,
#                 acknowledgment_date=acknowledgment_date,
#             )
#             return JsonResponse({'message': 'Purchase order created successfully'}, status=201)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    

# @csrf_exempt
# def get_vendor_performance(request, vendor_id):
#     if request.method == 'GET':
#         # Retrieve vendor by ID
#         try:
#             vendor = Vendor.objects.get(id=vendor_id)
#         except Vendor.DoesNotExist:
#             return JsonResponse({'error': 'Vendor not found'}, status=404)
        
#         # Get performance metrics
#         performance_metrics = {
#             'on_time_delivery_rate': vendor.on_time_delivery_rate,
#             'quality_rating_avg': vendor.quality_rating_avg,
#             'average_response_time': vendor.average_response_time,
#             'fulfillment_rate': vendor.fulfillment_rate
#         }
#         return JsonResponse(performance_metrics)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)