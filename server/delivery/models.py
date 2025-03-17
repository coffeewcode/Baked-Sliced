from django.db import models
from address.models import Address
import uuid

class DeliveryType(models.TextChoices):
    STORE_PICKUP = "store_pickup", "Store Pickup"
    DELIVERY = "delivery", "Delivery"

class DeliveryStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"

class Delivery(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    type = models.CharField(max_length=20, choices=DeliveryType.choices, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_time = models.CharField(max_length=30)
    observations = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING)
    
    def __str__(self):
        return f"Delivery {self.id} to {self.address.city} ({self.status})"