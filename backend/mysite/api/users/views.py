from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from .serializers import (ListSubscripSerializer, MyDjoserUserSerializer,
                          MyTokenCreateSerializer, SubscripUserSerializer)

# from rest_framework.views import APIView


User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    serializer_class = MyTokenCreateSerializer


class ListrAllUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyDjoserUserSerializer
    queryset = User.objects.all()

    def get_instance(self):
        if self.kwargs.get('id') is not None:
            return User.objects.get(id=self.kwargs.get('user_id'))
        
    def get_queryset(self):
        return self.request.user

    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




class ListSubscripViewSet(UserViewSet):
    serializer_class = ListSubscripSerializer

    def get_queryset(self):
        return User.objects.filter(
           following__user=self.request.user
        )


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = SubscripUserSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User,
                                   id=self.kwargs.get('subs_id'))
        serializer.save(user=self.request.user, author=author)
