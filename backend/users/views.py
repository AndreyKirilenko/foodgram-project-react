from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from foodgram.models import User
from foodgram.paginations import CustomPagination
from .models import Subscription
from .serializers import FullCustomUserSerializer, SubscriptionSerializer


class ListUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FullCustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(following__user=self.request.user)
        return queryset


class CreateDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.id == kwargs['id']:
            raise ValidationError(['Нельзя подписаться на самого себя'])
        if Subscription.objects.filter(
            user=self.request.user,
            author=kwargs['id']
        ):
            raise ValidationError(['Вы уже подписаны на этого автора'])

        user = self.request.user
        request.data.update({"user": user.id, "author": kwargs['id']})
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = User.objects.get(id=kwargs['id'])
        serializer = FullCustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        if self.request.user.id == kwargs['id']:
            raise ValidationError(['Вы не подписаны на самого себя'])
        subscribe = get_object_or_404(
            Subscription, user=self.request.user, author=kwargs['id']
        )
        subscribe.delete()
        return Response(
            'Вы отписаны от автора', status=status.HTTP_204_NO_CONTENT
        )
