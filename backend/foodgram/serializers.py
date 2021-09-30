from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Ingredients, Tag, Recipe, Quantity_ingredients, Favorite, Shopping_cart


class Shopping_cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_cart
        fields = ('__all__')

class TagSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    tags = TagSerialiser(many=True, read_only=True)
    class Meta:
        model = Recipe
        # field = '__all__'
        fields = ('id', 'name', 'image', 'text', 'cooking_time', 'author', 'tags', 'ingredients')