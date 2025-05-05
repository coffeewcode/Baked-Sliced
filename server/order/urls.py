from . import views
from django.urls import path


def order_include(view, suffix=""):
    return path(f"order/{suffix}", view)


urlpatterns = [
    order_include(views.OrderItemListView.as_view(), "list"),
    # order_include(views.OrderItemCreateView.as_view(), "create"),
    order_include(views.OrderItemDestroyView.as_view(), "delete/<uuid:id>"),
    order_include(views.OrderItemUpdateView.as_view(), "update/<uuid:id>"),
    order_include(
        views.OrderItemAdditionalDestroyView.as_view(), "additional/delete/<uuid:id>"
    ),
    order_include(
        views.OrderItemAdditionalUpdateView.as_view(), "additional/update/<uuid:id>"
    ),
    order_include(views.OrderItemAdditionalListView.as_view(), "additional/list"),
]
