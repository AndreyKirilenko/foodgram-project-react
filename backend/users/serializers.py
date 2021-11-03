import re
# from django.db.models import fields
# from django.db.models import fields
# from django.http import request

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
# from backend.foodgram.models import Recipe

from foodgram.models import Recipe
# from foodgram import serializers

from .models import CustomUser, Subscription


class CustomUserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            'is_subscribed'
            )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
            ).exists()

    def validate_username(self, value):
        if re.match('[\w]', value) is None:
            raise ValidationError(f'{value} не соответствует маске ')
        return value


class FollowRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FullCustomUserSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email", "id", "username", "first_name", "last_name",
            'is_subscribed', 'recipes', 'recipes_count',
            )

    def get_recipes(self, obj):
        request = self.context.get('request')

        if request is None:
            recipes = Recipe.objects.filter(author=obj)
            return FollowRecipeSerializer(recipes, many=True).data

        recipes_limit = request.query_params.get('recipes_limit', None)
        if recipes_limit is not None:
            recipes = Recipe.objects.filter(author=obj)[:int(recipes_limit)]
        else:
            recipes = Recipe.objects.filter(author=obj)
        return FollowRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ("__all__")
