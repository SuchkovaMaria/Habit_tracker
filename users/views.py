from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UsersCreateView(CreateAPIView):
    """Класс создания пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]

    def create(self, request, *args, **kwargs):
        data = request.data

        user = User.objects.create(**data)
        user.set_password(data.get("password"))
        user.save()
        return Response({"email": user.email}, status=status.HTTP_201_CREATED)
