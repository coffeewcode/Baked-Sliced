from rest_framework import generics
from .models import Delivery
from .serializers import DeliverySerializer

class DeliveryListView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class DeliveryCreateView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class DeliveryDetailView(generics.RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class DeliveryUpdateView(generics.UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class DeliveryDeleteView(generics.DestroyAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
