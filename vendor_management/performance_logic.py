from django.utils import timezone
from django.db.models import Count, Avg
from .models import PurchaseOrder

def calculate_on_time_delivery_rate(vendor_id):
    completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='completed')
    # print("completed_pos***************->",completed_pos)
    total_completed_pos = completed_pos.count()
    # print("total_completed_pos***************->", total_completed_pos)
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    # print("on_time_deliveries***************->", on_time_deliveries)

    if total_completed_pos == 0:
        return 0.0
    else:
        return (on_time_deliveries / total_completed_pos) * 100

def calculate_quality_rating_avg(vendor_id):
    # Filter completed purchase orders for the given vendor
    completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='completed')
    
    # Aggregate the average quality rating for completed purchase orders
    aggregation_result = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))
    print("aggregation_result---->",aggregation_result)
    # Access the calculated average quality rating from the aggregation result
    average_quality_rating = aggregation_result['avg_quality_rating']
    
    return average_quality_rating or 0.0

def calculate_average_response_time(vendor_id):
    completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='completed')
    
    response_times = []

    # Iterate over each completed purchase order
    for po in completed_pos:
        # Check if the purchase order has an acknowledgment date
        if po.acknowledgment_date:
            # Calculate the time difference between acknowledgment date and issue date
            time_difference_seconds = (po.acknowledgment_date - po.issue_date).total_seconds()
            # Convert time difference from seconds to hours and append to response_times list
            response_time_hours = time_difference_seconds / 3600
            response_times.append(response_time_hours)

    # Calculate the average response time
    if response_times:
        average_response_time = sum(response_times) / len(response_times)
    else:
        average_response_time = 0.0

    return average_response_time

def calculate_fulfillment_rate(vendor_id):
    total_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    successfully_fulfilled_pos = total_pos.filter(status='completed').count()
    print("total_pos----->",total_pos)
    print("successfully_fulfilled_pos----->",successfully_fulfilled_pos)
    if total_pos.count() == 0:
        return 0.0
    else:
        return (successfully_fulfilled_pos / total_pos.count()) * 100
