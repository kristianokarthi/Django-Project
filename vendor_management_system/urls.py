
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vendor_management.urls')), 
    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('API_Documentation/', TemplateView.as_view(template_name='API_Documentation.html'), name='API_Documentation'),
]
