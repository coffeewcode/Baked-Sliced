from django.shortcuts import render
from rest_framework import generics
from .serializer import AdditionalSerializer
from .models import Additional


class AdditionalListView(generics.ListAPIView):
    serializer_class = AdditionalSerializer
    queryset = Additional.objects.all()


class AdditionalListByStatus(generics.ListAPIView):
    serializer_class = AdditionalSerializer

    def get_queryset(self):
        status = self.request.query_params.get("status", "active")
        if status == "disabled":
            return Additional.objects.filter(is_active=False).order_by("name")
        return Additional.objects.filter(is_active=True).order_by("name")


class AdditionalListSoldOutView(generics.ListAPIView):
    serializer_class = AdditionalSerializer

    def get_queryset(self):
        return Additional.objects.filter(stock_quantity=0, is_active=False)


class AdditionalCreateView(generics.CreateAPIView):
    serializer_class = AdditionalSerializer
    queryset = Additional.objects.all()


class AdditionalDestroyView(generics.DestroyAPIView):
    serializer_class = AdditionalSerializer
    queryset = Additional.objects.all()
    lookup_field = "id"


class AdditionalUpdateView(generics.UpdateAPIView):
    serializer_class = AdditionalSerializer
    queryset = Additional.objects.all()
    lookup_field = "id"
