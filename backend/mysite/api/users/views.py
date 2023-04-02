from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import viewsets


User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

