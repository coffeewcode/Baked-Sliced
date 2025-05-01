from rest_framework.views import APIView
from product.models import Product
from rest_framework.response import Response
from .models import ShoppingCart, ShoppingCartItem, ShoppingCartItemAdditional
from additional.models import Additional
from rest_framework.generics import ListAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ShoppingCartSerializer


class AddItemsInShoppingCartView(APIView):
    def post(self, request):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")
        additional_items = request.data.get("additional_items")
        observation = request.data.get("observation")

        print(additional_items)
        product = get_object_or_404(Product, id=product_id)

        cart, _ = ShoppingCart.objects.get_or_create()

        shopping_cart_item = ShoppingCartItem.objects.create(
            shopping_cart=cart,
            product=product,
            quantity=quantity,
            observation=observation,
        )

        for item in additional_items:
            item_id = item.get("additional_id")
            item_quantity = item.get("quantity")

            additional = get_object_or_404(Additional, id=item_id)

            print(additional)
            ShoppingCartItemAdditional.objects.create(
                shopping_cart_item=shopping_cart_item,
                additional=additional,
                quantity=item_quantity,
            )

        return Response(
            {"message": "Item added to cart"}, status=status.HTTP_201_CREATED
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
