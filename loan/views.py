from rest_framework.generics import CreateAPIView
from .models import Loan
from .serializer import LoanSerializer
from rest_framework.permissions import (
    IsAdminUser,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from copies.models import Copy


class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.request.data.get("user_id")
        copy = User.objects.get(id=user_id)
        serializer.save(user=self.request.user, copy=copy)
