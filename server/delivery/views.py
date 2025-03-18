from rest_framework import generics
from .models import Delivery
from .serializers import DeliverySerializer

class DeliveryListView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

class DeliveryCreateView(generics.CreateAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    
class DeliveryDetailView(generics.RetrieveAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

class DeliveryUpdateView(generics.UpdateAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    
class DeliveryDeleteView(generics.DestroyAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    
