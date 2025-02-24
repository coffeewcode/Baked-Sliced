from django.shortcuts import render
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import (
    OrderItemListSerializer,
    OrderItemSerializer,
    OrderItemAdditionalSerializer,
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


class OrderItemPatchView(generics.UpdateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    lookup_field = "id"


class OrderItemAdditionalCreateView(generics.CreateAPIView):
    serializer_class = OrderItemAdditionalSerializer
    queryset = OrderItemAdditional.objects.all()

    def create(self, request):
        serializer = self.get_serializer(request=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
