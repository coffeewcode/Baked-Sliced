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


class OrderItemDestroyView(generics.DestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    lookup_field = "id"

    def perform_destroy(self, instance):
        if not instance.is_delivered and instance.product:
            instance.product.increment_stock(instance.quantity)
            for order_item_additional in instance.order_item_additional.all():
                if order_item_additional.additional:
                    order_item_additional.additional.increment_stock(
                        order_item_additional.quantity
                    )
        # TODO: its not possible to exclude an order when the delivery is in the way
        instance.delete()


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
