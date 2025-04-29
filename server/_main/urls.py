from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Baked Sliced",
        default_version="v1",
        description="""This project is a full-featured e-commerce system built 
        with Python, handling payments, order processing, inventory management,
        and admin operations through a modular backend architecture.""",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact.coffeewcode@gmail.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
