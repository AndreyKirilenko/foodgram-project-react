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


class Quantity_ingredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source = 'ingredient.id') # Взял значение из связанной модели Ingredients
    name = serializers.ReadOnlyField(source = 'ingredient.name') # Взял значение из связанной модели Ingredients
    measurement_unit = serializers.ReadOnlyField( # Взял значение из связанной модели Ingredients
        source = 'ingredient.measurement_unit'
    )
    
    class Meta:
        model = Quantity_ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = Quantity_ingredientsSerializer(
        source='amount', many=True, read_only=True, # Взял значение из модели Quantity_ingredients ?? Как?
    )
    author = CustomUserSerializer(read_only=True)
    tags = TagSerialiser(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 
            'tags', 
            'author', 
            'ingredients', 
            'is_favorited', 
            'is_in_shopping_cart', 
            'name', 
            'image', 
            'text', 
            'cooking_time', 
        )
    
    def get_ingredients(self, obj):
        qs = Quantity_ingredients.objects.filter(recipe=obj)

        # return IngredientSerializer(many=True, read_only=True).data
        # return IngredientSerializer(qs, many=True).data


    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if Favorite.objects.filter(user=request.user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if Shopping_cart.objects.filter(user=request.user, recipe=obj).exists():
            return True
        return False