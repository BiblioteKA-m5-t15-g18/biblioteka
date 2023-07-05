from rest_framework import generics
from .models import Loan
from .serializer import LoanSerializer
from rest_framework.permissions import (
    IsAdminUser,
)
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from copies.models import Copy
from users.models import User
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from users.permissions import IsAccountOnwer


class LoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.request.data.get("copy")
        copy = Copy.objects.get(id=copy_id)

        if copy.disponibilidade == False:
            raise ValidationError("A cópia não está disponível.")

        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)

        if user.block == True:
            raise ValidationError("O usuário está bloqueado.")

        copy.disponibilidade = False
        copy.save()

        prazo = self.calculate_prazo()
        loan = serializer.save(user=user, copy=copy, prazo=prazo)

        copy.loan = loan.id
        copy.save()

    def calculate_prazo(self):
        current_date = timezone.now()
        prazo = current_date + timedelta(days=7)

        if prazo.weekday() >= 5:
            prazo += timedelta(days=2)

        return prazo


class LoanDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_update(self, serializer):
        copy_id = self.request.data.get("copy")

        user_id = self.request.data.get("user")

        return serializer.save(
            user_id=user_id,
            copy_id=copy_id,
            loan_id=self.kwargs.get("pk"),
            block=self.request.data.get("block"),
        )
