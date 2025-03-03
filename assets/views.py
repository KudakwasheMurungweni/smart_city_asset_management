from django.shortcuts import render, redirect
from .models import Asset, MaintenanceLog
from django.db.models import Sum
import datetime
from django.db.models import Q
import plotly.graph_objects as go
from .forms import AssetForm



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

    # Create a Plotly bar chart
    categories = [entry['category'] for entry in report]
    costs = [entry['total_cost'] for entry in report]

    # Create the chart
    fig = go.Figure(data=[go.Bar(x=categories, y=costs)])

    # Update layout for the chart
    fig.update_layout(
        title='Total Asset Cost by Category',
        xaxis_title='Asset Category',
        yaxis_title='Total Cost',
        template='plotly_dark'
    )

    # Get the HTML representation of the plot
    chart = fig.to_html(full_html=False)

    return render(request, '../templates/cost_report.html', {'report': report, 'chart': chart})


def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')  # Redirect to asset list page after saving the asset
    else:
        form = AssetForm()

    return render(request, '../templates/add_asset.html', {'form': form})