from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import CustomFilter
from .models import (Favorite, Ingredient, QuantityIngredient, Recipe,
                     Shopping_cart, Tag)
from .paginations import CustomPagination
from .permissions import IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          SmallRecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backend = (DjangoFilterBackend, )
    filterset_class = CustomFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    @action(
        methods=['get', 'delete'],
        detail=False,
        url_path='(?P<id>[0-9]+)/shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def add_delete_shopping_cart(self, request, **kwargs):
        check_exist = Shopping_cart.objects.filter(
            user=self.request.user, recipe=kwargs['id']
        ).exists()

        if request.method == 'DELETE':
            if check_exist:
                get_object_or_404(
                    Shopping_cart, user=self.request.user, recipe=kwargs['id']
                ).delete()
                return Response(
                    'Рецепт успешно удален из списка покупок',
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    'Рецепта нет в списке покупок',
                    status=status.HTTP_400_BAD_REQUEST
                )
        if check_exist:
            return Response(
                'Рецепт уже есть в списке покупок',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.request.user
        request.data.update({"user": user.id, "recipe": kwargs['id']})
        serializer = ShoppingCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        serializer = SmallRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['get', 'delete'],
        detail=False,
        url_path='(?P<id>[0-9]+)/favorite',
        permission_classes=[IsAuthenticated]
    )
    def add_delete_favorite(self, request, **kwargs):
        check_exist = Favorite.objects.filter(
            user=self.request.user, recipe=kwargs['id']
        ).exists()

        if request.method == 'DELETE':
            if check_exist:
                get_object_or_404(
                    Favorite, user=self.request.user, recipe=kwargs['id']
                ).delete()
                return Response(
                    'Рецепт успешно удален из избранного',
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    'Рецепта нет в избранном',
                    status=status.HTTP_400_BAD_REQUEST
                )
        if check_exist:
            return Response(
                'Рецепт уже есть в избранном',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.request.user
        request.data.update({'user': user.id, 'recipe': kwargs['id']})
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        serializer = SmallRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request):
        """Создает файл с рецептами и ингредиентами для списка покупок"""
        list_recipe = Recipe.objects.filter(
            shoping_cart__user=self.request.user
        ).values_list('id', flat=True)
        list_quantity_ingredient = QuantityIngredient.objects.filter(
            recipe__in=list_recipe
        )
        list_ingredients = {}
        for quantity_ingredient in list_quantity_ingredient:
            ingredient = quantity_ingredient.ingredient
            if ingredient.name in list_ingredients:
                list_ingredients[ingredient.name][
                    'amount'] += quantity_ingredient.amount
            else:
                list_ingredients[ingredient.name] = {
                    'unit': ingredient.measurement_unit,
                    'amount': quantity_ingredient.amount
                }

        list_recipes = Recipe.objects.filter(
            shoping_cart__user=self.request.user
        ).values_list('name', flat=True)

        """собираем список рецептов"""
        list_resipes_result = {}
        for recipe in list_recipes:
            if recipe in list_resipes_result:
                list_resipes_result[recipe]['count'] += 1
            else:
                list_resipes_result[recipe] = {
                    'count': 1
                }
        recipes_string = ''
        for item in list_resipes_result:
            recipes_string += (
                str(item) + ' - ' + str(list_resipes_result[item]['count'])
                + '\n'
            )
        """собираем список ингредиентов"""
        ingredients_string = ''
        for item in list_ingredients:
            ingredients_string += (
                str(item) + ' (' + str(list_ingredients[item]['unit'])
                + ') - ' + str(list_ingredients[item]['amount']) + '\n'
            )
        if list_resipes_result == {}:
            response = (
                'Для отображения ингредиентов,\
                добавте рецепты в список покупок'
            )
        else:
            response = (
                f'Список рецептов в корзине: \n \n{recipes_string} \
                \nДля приготовления понадобятся: \n \n{ingredients_string} \
                \n \n -- foodgram --')
        response = HttpResponse(response, 'Content-Type: application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart"'
        )
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
