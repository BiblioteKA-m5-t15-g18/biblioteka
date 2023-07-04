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
from loan.models import Loan
from loan.serializer import LoanSerializer
from django.shortcuts import get_object_or_404


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserHistoricDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAccountOnwer]

    queryset = User.objects.all()
    serializer_class = UserHistoricSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return User.objects.filter(id=user_id)


class UserFollowDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAccountOnwer]

    queryset = User.objects.all()
    serializer_class = UserDetailFollowingSerializer
