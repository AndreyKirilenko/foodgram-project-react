from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredients, Quantity_ingredients, Recipe,
                     Shopping_cart, Tag)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('__all__')


class Shopping_cartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shopping_cart
        fields = ('id', 'user', 'recipe')


class FaviriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')


class TagSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Quantity_ingredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = Quantity_ingredients
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
    ingredients = Quantity_ingredientsSerializer(
        source='amount', many=True, read_only=True
    )
    author = CustomUserSerializer(read_only=True)
    tags = TagSerialiser(many=True, read_only=True)
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
        ''''Показывает есть ли рецепт в избраном у текущего юзера'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if Favorite.objects.filter(user=request.user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        ''''Показывает есть ли рецепт в списке покупок у текущего юзера'''
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if Shopping_cart.objects.filter(
            user=request.user, recipe=obj
        ).exists():
            return True
        return False

    def create(self, validated_data):
        ''''Переопределяем для сохранения ингредиентов и тегов'''
        image = validated_data.pop('image')
        author = self.context['request'].user
        recipe = Recipe.objects.create(
            image=image, author=author, **validated_data
            )

        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            Quantity_ingredients.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount')
            )

        tags = self.initial_data.get('tags')
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

        return recipe

    def update(self, instance, validated_data):
        ''''Переопределяем для сохранения ингредиентов и тегов'''
        # import pdb; pdb.set_trace()
        instance.author = validated_data.get('author', instance.author)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
            )

        instance.tags.clear()
        tags = self.initial_data.get('tags')
        for tag in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag))

        instance.ingredients.clear()
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            Quantity_ingredients.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=instance,
                amount=ingredient.get('amount')
            )
        instance.save()
        return instance
