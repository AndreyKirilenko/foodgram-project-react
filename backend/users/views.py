# from rest_framework import serializers
from rest_framework import generics
# from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from foodgram.paginations import CustomPagination

from foodgram.models import User
from .serializers import CustomUserSerializer, FullCustomUserSerializer
from rest_framework.response import Response

from .models import Subscription


class ListUsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FullCustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        # user = self.request.user
        queryset = queryset.filter(following__user=self.request.user)
        return queryset

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)


class CreateDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
