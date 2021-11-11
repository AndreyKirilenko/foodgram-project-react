from django.http import HttpResponse
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly

from .filters import CustomFilter
from .models import (Favorite, Ingredients, Quantity_ingredients, Recipe,
                     Shopping_cart, Tag)
from .paginations import CustomPagination
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, Shopping_cartSerializer,
                          SmallRecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_class = CustomFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        '''Фильтрация по избранному для авторизованых'''
        is_favorited = self.request.query_params.get('is_favorited', None)
        if is_favorited is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(favorite__user=self.request.user)
        ''''Фильтрация по списку покупок для авторизованых'''
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart', None
        )
        if is_in_shopping_cart is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(shoping_cart__user=self.request.user)
        return queryset

    @action(
        methods=['get', 'delete'],
        detail=False,
        url_path='(?P<id>[0-9]+)/shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def add_delete_shopping_cart(self, request, **kwargs):
        # import pdb; pdb.set_trace()
        item = Shopping_cart.objects.filter(
            user=self.request.user, recipe=kwargs['id']
        ).exists()

        if request.method == 'DELETE':
            if item:
                Shopping_cart.objects.get(
                    user=self.request.user, recipe=kwargs['id']
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
        if item:
            return Response(
                'Рецепт уже есть в списке покупок',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.request.user
        request.data.update({"user": user.id, "recipe": kwargs['id']})
        serializer = Shopping_cartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        recipe = self.queryset.get(id=kwargs['id'])
        serializer = SmallRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['get', 'delete'],
        detail=False,
        url_path='(?P<id>[0-9]+)/favorite',
        permission_classes=[IsAuthenticated]
    )
    def add_delete_favorite(self, request, **kwargs):
        # import ipdb; ipdb.set_trace()
        item = Favorite.objects.filter(
            user=self.request.user, recipe=kwargs['id']
        ).exists()

        if request.method == 'DELETE':
            if item:
                Favorite.objects.get(
                    user=self.request.user, recipe=kwargs['id']
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
        if item:
            return Response(
                'Рецепт уже есть в избранном',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.request.user
        request.data.update({"user": user.id, "recipe": kwargs['id']})
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        recipe = self.queryset.get(id=kwargs['id'])
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
        )
        list_ingredients = {}
        for recipe in list_recipe:
            ingredients = Quantity_ingredients.objects.filter(recipe=recipe)
            for item in ingredients:
                name = item.ingredient
                if name.name in list_ingredients:
                    list_ingredients[name.name]['amount'] += item.amount
                else:
                    list_ingredients[name.name] = {
                        'unit': item.ingredient.measurement_unit,
                        'amount': item.amount
                    }
        list_resipes = ''
        for recipe in list_recipe:
            list_resipes += ' ' + str(recipe) + '\n'
        ingredients_string = ''
        for item in list_ingredients:
            ingredients_string += (
                    str(item) + ' (' + str(list_ingredients[item]['unit']) \
                    + ') - ' + str(list_ingredients[item]['amount']) + '\n'
            )
        if list_resipes == '':
            response = (
                'Для отображения ингредиентов,\
                добавте рецепты в список покупок'
            )
        else:
            response = (
                f'Список ваших рецептов: \n \n{list_resipes} \
                \nДля приготовления понадобятся: \n \n{ingredients_string} \
                \n \n -- foodgram --')
        response = HttpResponse(response, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart"'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredients.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
