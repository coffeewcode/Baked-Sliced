from django.forms import ValidationError
from rest_framework.views import APIView
from product.models import Product
from rest_framework.response import Response
from .models import ShoppingCart, ShoppingCartItem, ShoppingCartItemAdditional
from additional.models import Additional
from rest_framework.generics import ListAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ShoppingCartItemSerializer, ShoppingCartSerializer


class AddItemsInShoppingCartView(APIView):
    def post(self, request):
        serializer = ShoppingCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        product_id = request.data.get("product")
        quantity = request.data.get("quantity")
        additional_items = request.data.get("additionals")
        observation = request.data.get("observation")

        product = get_object_or_404(Product, id=product_id)

        cart, _ = ShoppingCart.objects.get_or_create()

        shopping_cart_item = ShoppingCartItem.objects.create(
            shopping_cart=cart,
            product=product,
            quantity=quantity,
            observation=observation,
        )

        for item in additional_items:
            item_id = item.get("additional")
            item_quantity = item.get("quantity")

            self.__validate_additional_requirements(quantity, additional)

            additional = get_object_or_404(Additional, id=item_id)

            ShoppingCartItemAdditional.objects.create(
                shopping_cart_item=shopping_cart_item,
                additional=additional,
                quantity=item_quantity,
            )

        return Response(
            {"message": "Item added to cart"}, status=status.HTTP_201_CREATED
        )

    def __validate_additional_requirements(self, quantity, additionals):
        if quantity > 0 and additionals:
            raise ValidationError(
                "The field quantity needs to be grather than 0 to add an additional"
            )


class OrderItemAdditionalDestroyView(DestroyAPIView):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    lookup_field = "id"


class CheckoutShoppingCartView(APIView):
    # TODO: use the user from request instead shopping_cart_id
    def post(self, request, id):
        shopping_cart_id = id
        shopping_cart = get_object_or_404(ShoppingCart, id=shopping_cart_id)
        order = shopping_cart.convert_to_order()
        return Response(
            {"message": "Order created successfully.", "order_id": order.id},
            status=status.HTTP_201_CREATED,
        )


class ShoppingCartListView(ListAPIView):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
