from django.shortcuts import render
from .models import Asset, MaintenanceLog
from django.db.models import Sum
import datetime
from django.db.models import Q
 



def home(request):
    return render(request, '../templates/home.html')


def asset_list(request):
    role = request.GET.get('role', 'Worker')  # Default to Worker if no role is selected
    search_query = request.GET.get('search', '')  # Search filter

    # Role-based asset filtering
    if role == 'Worker':
        assets = Asset.objects.filter(condition__in=['Good', 'Fair'])
    elif role == 'Supervisor':
        assets = Asset.objects.all()  # Supervisor sees all assets
    elif role == 'Manager':
        assets = Asset.objects.all()  # Manager sees all assets + cost report

    # Search filter: filter by name, category, condition, or status
    if search_query:
        assets = assets.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(condition__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    return render(request, '../templates/asset_list.html', {'assets': assets, 'role': role, 'search_query': search_query})

def maintenance_report(request):
    # Show assets with a condition of 'Poor' or 'Critical'
    report_assets = Asset.objects.filter(condition__in=['Poor', 'Critical'])
    maintenance_logs = MaintenanceLog.objects.filter(asset__in=report_assets)
    return render(request, '../templates/maintenance_report.html', {'assets': report_assets})

def cost_report(request):
    # Group assets by category and summarize total cost
    report = Asset.objects.values('category').annotate(total_cost=Sum('cost'))
    return render(request, '../templates/cost_report.html', {'report': report})
