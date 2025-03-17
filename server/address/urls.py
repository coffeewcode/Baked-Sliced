from . import views
from django.urls import path 

def address_include(view, suffix=""):
    return path(f"address/{suffix}", view)

urlpatterns = [
    address_include(views.AddressListView.as_view(), "list"),
    address_include(views.AddressCreateView.as_view(), "create"),
    address_include(views.AddressDetailView.as_view(), "<uuid:pk>"),
    address_include(views.AddressUpdateView.as_view(), "update/<uuid:pk>"),
    address_include(views.AddressDeleteView.as_view(), "delete/<uuid:pk>"),
]