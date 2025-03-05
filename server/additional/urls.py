from . import views
from django.urls import path


def additional_include(view, suffix=""):
    return path(f"additional/{suffix}", view)


urlpatterns = [
    additional_include(views.AdditionalListView.as_view(), "list"),
    additional_include(views.AdditionalListByStatus.as_view(), "list-by-status"),
    additional_include(views.AdditionalListSoldOutView.as_view(), "sold-out"),
    additional_include(views.AdditionalCreateView.as_view(), "create"),
    additional_include(views.AdditionalDestroyView.as_view(), "delete/<uuid:id>"),
    additional_include(views.AdditionalUpdateView.as_view(), "update/<uuid:id>"),
]
