import re
from django.db.models import fields

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


class MiniRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FullCustomUserSerializer(CustomUserSerializer):
    recipes = MiniRecipeSerializer(source='recipe', many=True, read_only=True
    )
    # recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            'is_subscribed',
            'recipes',
            )

    # def get_recipes(self, obj):
    #     pass

