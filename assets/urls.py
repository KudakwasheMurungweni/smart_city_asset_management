from django.urls import path
from .views import home, asset_list, maintenance_report, cost_report, add_asset

urlpatterns = [
    path('', home, name='home'),  # Add homepage route
    path('assets/', asset_list, name='asset_list'),
    path('maintenance-report/', maintenance_report, name='maintenance_report'),
    path('cost-report/', cost_report, name='cost_report'),
    path('add-asset/', add_asset, name='add_asset'), 
]
