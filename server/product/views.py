from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics
from .serializer import ProductSerializer
from .models import Product


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductListByStatusView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        status = self.request.query_params.get("status", "active")
        if status == "disabled":
            return Product.objects.filter(is_active=False).order_by("name")
        return Product.objects.filter(is_active=True).order_by("name")


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)


class ProductDestroyView(generics.DestroyAPIView):
    querysets = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def perform_destroy(self, instance: Product) -> None:
        if instance.is_active:
            raise ValidationError(
                f"The product {instance.name} is active. Disable its to delete."
            )
        return super().perform_destroy(instance)


class ProductPatchView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_active and instance.quantity <= 0:
            raise ValidationError("Active products must have a positive stock")
        if instance.quantity == 0:
            instance.is_active = False
            instance.save()
        return instance


class ProductListSoldOut(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(quantity=0, is_active=False)
