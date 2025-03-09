from rest_framework import generics
from .serializer import (
    OrderItemAdditionalListSerializer,
    OrderItemAdditionalUpdateSerializer,
    OrderItemListSerializer,
    OrderItemSerializer,
    OrderItemAdditionalSerializer,
    OrderItemUpdateSerializer,
)
from .models import OrderItem, OrderItemAdditional


class OrderItemListView(generics.ListAPIView):
    serializer_class = OrderItemListSerializer
    queryset = OrderItem.objects.all()


class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class OrderItemDestroyView(generics.DestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    lookup_field = "id"


class OrderItemUpdateView(generics.UpdateAPIView):
    serializer_class = OrderItemUpdateSerializer
    queryset = OrderItem.objects.all()
    lookup_field = "id"


class OrderItemAdditionalDestroyView(generics.DestroyAPIView):
    serializer_class = OrderItemAdditionalSerializer
    queryset = OrderItemAdditional.objects.all()
    lookup_field = "id"


class OrderItemAdditionalListView(generics.ListAPIView):
    serializer_class = OrderItemAdditionalListSerializer
    queryset = OrderItemAdditional.objects.all()


class OrderItemAdditionalUpdateView(generics.UpdateAPIView):
    serializer_class = OrderItemAdditionalUpdateSerializer
    queryset = OrderItemAdditional.objects.all()
    lookup_field = "id"
