from . import views
from django.urls import path


def shopping_cart_include(view, suffix=""):
    return path(f"shopping_cart/{suffix}", view)


urlpatterns = [
    shopping_cart_include(views.AddItemsInShoppingCartView.as_view(), "add_item"),
    shopping_cart_include(
        views.CheckoutShoppingCartView.as_view(), "checkout/<uuid:id>"
    ),
    shopping_cart_include(
        views.OrderItemAdditionalDestroyView.as_view(), "delete/<uuid:id>"
    ),
    shopping_cart_include(views.ShoppingCartListView.as_view(), "list"),
]
