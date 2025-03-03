from django.db import models

class Asset(models.Model):
    CATEGORY_CHOICES = [
        ('Infrastructure', 'Infrastructure'),  # e.g., Roads, Bridges
        ('Equipment', 'Equipment'),            # e.g., Machinery, Vehicles
        ('Utility', 'Utility'),                # e.g., Streetlights, Pipes
    ]
    CONDITION_CHOICES = [
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
        ('Critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('In Use', 'In Use'),
        ('Under Maintenance', 'Under Maintenance'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='Good')
    purchase_date = models.DateField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.name} ({self.category})"


class MaintenanceLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_logs')
    date = models.DateField()
    details = models.TextField()
    status = models.CharField(max_length=30, choices=Asset.STATUS_CHOICES, default='Under Maintenance')

    def __str__(self):
        return f"Maintenance on {self.asset.name} - {self.date}"
