from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer

class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    
class AddressDetailView(generics.RetrieveAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    
class AddressUpdateView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    
class AddressDeleteView(generics.DestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    