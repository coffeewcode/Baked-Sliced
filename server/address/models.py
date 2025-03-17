from django.db import models
import uuid

class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=20)
    num = models.CharField(max_length=10)
    street = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30, null=True, blank=True)
    observations = models.CharField(max_length=200, blank=True)
    complement = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name}, {self.street}"

