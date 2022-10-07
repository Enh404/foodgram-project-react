from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Tag, Ingredient, Recipe, NumberOfIngredients, Favorite, ShoppingCart
)
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeListSerializer,
    RecipeWriteSerializer, FavoriteSerializer, ShoppingCartSerializer
)
from .permissions import IsOwnerOrReadOnly
from .pagination import CustomPageNumberPagination
from .filters import IngredientSearchFilter, RecipeFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeWriteSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shoping_list = {}
        ingredients = NumberOfIngredients.objects.filter(
            recipe__carts__user=request.user).values_list(
                'ingredient__name', 'ingredient__measurement_unit',
                'amount', 'recipe__name'
        )

        for obj in ingredients:
            ingredient = obj[0]
            if ingredient not in shoping_list:
                shoping_list[ingredient] = {
                    'measurement_unit': obj[1],
                    'amount': obj[2]
                }
            else:
                shoping_list[ingredient]['amount'] += obj[2]
        download_list = f'Список покупок пользователя {request.user.username}:'

        for ingredient in shoping_list:
            download_list += (
                f'{ingredient} '
                f'({shoping_list[ingredient]["measurement_unit"]}) '
                f'- {shoping_list[ingredient]["amount"]}\n'
            )
        response = HttpResponse(
            download_list,
            content_type='text/plain;charset=UTF-8',
        )
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_list.txt"'
        )
        return response
