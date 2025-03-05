from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(["GET"])
def test_api(request):
    return Response(
        {"success": "The api is connected and working"}, status=status.HTTP_200_OK
    )

def api_include(module):
    return path("api/", include(module))

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test", test_api),
    api_include("product.urls"),
    api_include("order.urls"),
    api_include("additional.urls"),
    api_include("address.urls"), 
    api_include("delivery.urls"),
]