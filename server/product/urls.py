from . import views
from django.urls import path


def products_include(view, suffix=""):
    return path(f"product/{suffix}", view)


urlpatterns = [
    products_include(views.ProductListView.as_view(), "list"),
    products_include(views.ProductListByStatusView.as_view(), "list-by-status"),
    products_include(views.ProductCreateView.as_view(), "create"),
    products_include(views.ProductDestroyView.as_view(), "delete/<uuid:id>"),
    products_include(views.ProductPatchView.as_view(), "update/<uuid:id>"),
    products_include(views.ProductListSoldOut.as_view(), "sold-out"),
    products_include(views.CategoryListView.as_view(), "category/list"),
    products_include(views.CategoryCreateView.as_view(), "category/create"),
    products_include(views.CategoryPatchView.as_view(), "category/update/<uuid:id>"),
    products_include(views.CategoryDestroyView.as_view(), "category/delete/<uuid:id>"),
]
