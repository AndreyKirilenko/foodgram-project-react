from django.shortcuts import render

from django.shortcuts import get_object_or_404
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
# from .filters import TagFilter
from rest_framework import filters, mixins, status, viewsets
from rest_framework import permissions
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import NOT, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import CustomFilter
from .paginations import CustomPagination
# from rest_framework.permissions import IsAuthenticated
from foodgram.permissions import (
    IsAuthenticatedOrReadOnly, 
    IsAuthorOrReadOnly
)
from rest_framework.pagination import LimitOffsetPagination
# from .filters import TitleFilter
from .models import Ingredients, Tag, Recipe, Quantity_ingredients, Favorite, Shopping_cart
from .serializers import (RecipeSerializer, Shopping_cartSerializer, TagSerialiser)

import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas

# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf', "UTF-8"))


from rest_framework.decorators import action

from django.conf import settings
from django.template.loader import render_to_string
# import weasyprint

import pdfkit
from django.http import HttpResponse


from django.template.loader import get_template
from django.template import Context

from io import StringIO

import xhtml2pdf.pisa as pisa

import os
from django.template.loader import get_template 
from django.template import Context

class Shopping_cartViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                        #    mixins.CreateModelMixin,
                           mixins.DestroyModelMixin
                           ):
    permission_classes = [IsAuthenticated]
    queryset = Shopping_cart.objects.all()
    serializer_class = Shopping_cartSerializer

    def list(self, request, *args, **kwargs):
        if Shopping_cart.objects.filter(user=self.request.user, recipe=kwargs['id']).exists():
            # import pdb; pdb.set_trace()
            return Response('Рецепт уже есть в списке покупок', status=status.HTTP_400_BAD_REQUEST)
        
        # import pdb; pdb.set_trace()
        user = self.request.user
        recipe = Shopping_cart.objects.filter(recipe=kwargs['id'])
        request.data.update({"user": user.id, "recipe": kwargs['id']})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()




class FavoriteViewSet(viewsets.ModelViewSet):
    pass


class Quantity_ingredientsViewSet(viewsets.ModelViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_class = CustomFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):

        queryset = Recipe.objects.all()

        '''Фильтрация по избранному для авторизованых'''
        is_favorited = self.request.query_params.get('is_favorited', None)
        if is_favorited is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(favorite__user=self.request.user)

        ''''Фильтрация по списку покупок для авторизованых'''
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart', None)
        if is_in_shopping_cart is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(shoping_cart__user=self.request.user)
        
        return queryset




    # def perform_update(self, serializer):
    #     user_instance = serializer.instance # Модифицируемый объект
        
    #     joined_ingr_recipes=Quantity_ingredients.objects.filter(recipe=user_instance)
    #     for joined in joined_ingr_recipes: # Удаляем связь ингредиента с рецептом
    #         joined.delete()
    #     # import pdb; pdb.set_trace()
    #     ingredients = self.request.data['ingredients'] # Вынаем список ингридиентов из реквеста
    #     for ingredient in ingredients: # Прописываем соответствие рецепта ингредиенту и кол-во
    #         Quantity_ingredients.objects.create(
    #             ingredient_id= ingredient['id'],
    #             recipe=user_instance,
    #             amount=ingredient['amount'],
    #         )

    #     tags = self.request.data['tags']

        # serializer.save()

    # @action(
    #     methods=['get'], 
    #     detail=False, 
    #     url_path='(?P<id>[0-9]+)/shopping_cart', 
    #     permission_classes=[IsAuthenticated]
    # )
    # def add_shopping_cart(self, request, *args, **kwargs):
    #     # if Shopping_cart.objects.filter(user=self.request.user, recipe=kwargs['id']).exists:
    #     #     import pdb; pdb.set_trace()
    #     #     return Response('Рецепт уже есть в списке покупок', status=status.HTTP_400_BAD_REQUEST)

    #     recipe = get_object_or_404(Recipe, id=kwargs['id'])
    #     # import pdb; pdb.set_trace()
    #     response = Shopping_cart.objects.create(user=self.request.user, recipe=recipe)

    #     # import pdb; pdb.set_trace()
    #     # response = Recipe.objects.get(id=kwargs['id'])
        

    #     serializer = self.get_serializer(data=response)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(
        methods=['get'], 
        detail=False, 
        url_path='download_shopping_cart', 
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request):
        '''Получаем рецепты и ингредиенты для списка покупок'''
        list_recipe = Recipe.objects.filter(shoping_cart__user=self.request.user)
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
        '''Получаем строки из списков'''
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
            response = 'Для отображения ингредиентов, добавте рецепты в список покупок'
        else:
            response = (
                f'Список ваших рецептов: \n \n{list_resipes} \
                \nДля приготовления понадобятся: \n \n{ingredients_string} \
                \n \n -- foodgram --')
        response = HttpResponse(response, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart"'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerialiser
    queryset = Tag.objects.all()



class IngredientsViewSet(viewsets.ModelViewSet):
    pass