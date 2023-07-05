from .models import User
from .serializers import (
    UserSerializer,
    UserHistoricSerializer,
    UserDetailFollowingSerializer,
)
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    IsAdminUser,
)
from .permissions import IsAccountOnwer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Usuários"])
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["Usuários"])
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["Histórico de empréstimos"])
class UserHistoricDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAccountOnwer]

    queryset = User.objects.all()
    serializer_class = UserHistoricSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return User.objects.filter(id=user_id)


@extend_schema(tags=["Livros seguidos"])
class UserFollowDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAccountOnwer]

    queryset = User.objects.all()
    serializer_class = UserDetailFollowingSerializer
