from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status
from .serializer import ProductSerializer, ProductListSerializer, CategorySerializer
from .models import Product, Category
from rest_framework.response import Response


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductListByStatusView(generics.ListAPIView):
    serializer_class = ProductListSerializer

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
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def perform_destroy(self, instance):
        if instance.is_active:
            raise ValidationError(
                f"The product {instance.name} is active. Disable it to delete."
            )
        return super().perform_destroy(instance)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class ProductPatchView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_active and instance.stock_quantity <= 0:
            raise ValidationError("Active products must have a positive stock")
        if instance.stock_quantity == 0:
            instance.is_active = False
            instance.save()
        return instance


class ProductListSoldOut(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(stock_quantity=0, is_active=False)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer


class CategoryPatchView(generics.UpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"


class CategoryDestroyView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
