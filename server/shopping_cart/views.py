from rest_framework.views import APIView
from product.models import Product
from rest_framework.response import Response
from models import ShoppingCart, ShoppingCartItem, ShoppingCartItemAdditional
from additional.models import Additional
from rest_framework.generics import ListAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from serializers import ShoppingCartSerializer


class AddItemsInShoppingCartView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")
        additional_items = request.data.get("additional_items")

        product = get_object_or_404(Product, id=product_id)

        cart, _ = ShoppingCart.objects.get_or_create(user=user)

        shopping_cart_item = ShoppingCartItem.objects.create(
            shopping_cart=cart,
            product=product,
            quantity=quantity,
        )

        for item in additional_items:
            item_id = item.get("additional_item")
            item_quantity = item.get("quantity")

            additional = get_object_or_404(Additional, id=item_id)

            ShoppingCartItemAdditional.objects.create(
                shopping_cart_item=shopping_cart_item,
                additional=additional,
                quantity=item_quantity,
            )

        return Response(
            {"message": "Item added to cart"}, status=status.HTTP_201.CREATED
        )


class OrderItemAdditionalDestroyView(DestroyAPIView):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    lookup_field = "id"


class CheckoutShoppingCartView(APIView):
    def post(self, request):
        user = request.user
        shopping_cart = get_object_or_404(ShoppingCart, user=user)
        order = shopping_cart.convert_to_order()
        return Response(
            {"message": "Order created successfully.", "order_id": order.id},
            status=status.HTTP_201_CREATED,
        )


class ShoppingCartListView(ListAPIView):
    serializer_class = ShoppingCartSerializer()
    queryset = ShoppingCart.objects.all()
