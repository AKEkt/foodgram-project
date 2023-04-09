from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.serializers import MyDjoserUserSerializer
from .models import Follow
from .serializers import (MyTokenCreateSerializer,
                          SubscripUserSerializer)

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class CustomUsersViewSet(UserViewSet):
    serializer_class = MyDjoserUserSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        methods=('get',), )
    def me(self, request):
        instance = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ListSubscripViewSet(UserViewSet):
    serializer_class = SubscripUserSerializer

    def get_queryset(self):
        return Follow.objects.filter(
           user=self.request.user
        )


class FollowViewSet(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = SubscripUserSerializer
    queryset = Follow.objects.all()
    http_method_names = ['post', 'delete']

    def perform_create(self, serializer):
        author = get_object_or_404(User,
                                   id=self.kwargs.get('pk'))
        serializer.save(user=self.request.user, author=author)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        follow_user = Follow.objects.filter(user=self.request.user,
                                            author=author)
        if follow_user.exists():
            follow_user.delete()
            return Response(
                {
                    'выполнено': 'Успешная отписка'
                }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                'ошибка': 'Объект не найден'
            }, status=status.HTTP_400_BAD_REQUEST)
