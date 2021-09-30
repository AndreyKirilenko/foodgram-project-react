from rest_framework import serializers
from .models import CustomUser, Subscription
from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ValidationError
import re



class CustomUserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model=CustomUser
        fields=("id", "username", "first_name", "last_name", "email", "password", 'is_subscribed' )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, author=obj).exists()

    def validate_username(self, value):
        if re.match('[\w]', value) is None:
            raise ValidationError(f'{value} не соответствует маске ')            
        return value