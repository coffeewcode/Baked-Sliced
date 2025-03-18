from . import views
from django.urls import path


def delivery_include(view, suffix=""):
    return path(f"delivery/{suffix}", view)


urlpatterns = [
    delivery_include(views.DeliveryListView.as_view(), "list"),
    delivery_include(views.DeliveryCreateView.as_view(), "create"),
    delivery_include(views.DeliveryDetailView.as_view(), "<uuid:pk>"),
    delivery_include(views.DeliveryUpdateView.as_view(), "update/<uuid:pk>"),
    delivery_include(views.DeliveryDeleteView.as_view(), "delete/<uuid:pk>"),
]