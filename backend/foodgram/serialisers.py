from rest_framework import serializers

from .models import Ingredients, Tag, Recipe, Quantity_ingredients, Favorite, Shopping_cart


class Shopping_cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_cart
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'