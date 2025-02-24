from . import views
from django.urls import path


def order_include(view, suffix=""):
    return path(f"order/{suffix}", view)


urlpatterns = [
    order_include(views.OrderItemListView.as_view(), "list"),
    order_include(views.OrderItemCreateView.as_view(), "create"),
    order_include(views.OrderItemDestroyView.as_view(), "delete/<uuid:id>"),
    order_include(views.OrderItemPatchView.as_view(), "update/<uuid:id>"),
    order_include(views.OrderItemAdditionalCreateView.as_view(), "additional/create"),
]
