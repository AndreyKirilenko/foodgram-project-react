from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users.serializers import CustomUserSerializer
from .models import (Favorite, Ingredient, QuantityIngredient, Recipe,
                     Shopping_cart, Tag)
from .utils import save_tags_and_ingredients


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_cart
        fields = ('id', 'user', 'recipe')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class QuantityIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = QuantityIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class SmallRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = QuantityIngredientSerializer(
        source='amount', many=True, read_only=True
    )
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

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

    def get_is_favorited(self, obj):
        """Показывает есть ли рецепт в избраном у текущего юзера"""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """'Показывает есть ли рецепт в списке покупок у текущего юзера"""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Shopping_cart.objects.filter(
                user=request.user, recipe=obj
        ).exists()

    def create(self, validated_data):
        """'Переопределяем для сохранения ингредиентов и тегов"""
        image = validated_data.pop('image')
        author = self.context['request'].user
        recipe = Recipe.objects.create(
            image=image, author=author, **validated_data
        )
        save_tags_and_ingredients(self, recipe)
        return recipe

    def update(self, instance, validated_data):
        """'Переопределяем для сохранения ингредиентов и тегов"""
        instance.tags.clear()
        instance.ingredients.clear()
        save_tags_and_ingredients(self, instance)
        return super().update(instance, validated_data)

    def validate(self, data):
        errors = []
        if type(data['cooking_time']) is int:
            if data['cooking_time'] < 1:
                errors.append('Время приготовления меньше 1')
        else:
            errors.append('Время приготовления не является числом')

        tags = self.initial_data.get('tags')
        uniq_tag = [0]
        for tag in tags:
            if uniq_tag[-1] == tag:
                errors.append('Вы добавили одинаковые теги')
                break
            uniq_tag.append(tag)

        ingredients = self.initial_data.get('ingredients')
        uniq_ingr = [0]
        for ingredient in ingredients:
            if ingredient['amount'] < 1:
                errors.append('Колличество ингредиента не может быть меньше 1')
            if uniq_ingr[-1] == ingredient['id']:
                errors.append('Вы добавили одинаковые ингредиенты')
            uniq_ingr.append(ingredient['id'])

        if errors:
            raise ValidationError(errors)
        return data
