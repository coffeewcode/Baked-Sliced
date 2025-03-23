from django.urls import path


def shopping_cart_include(view, suffix=""):
    return path(f"product/{suffix}", view)


# urlpatterns = [
#   shopping_cart_include()
# ]
