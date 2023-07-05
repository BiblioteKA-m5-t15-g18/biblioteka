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

        if copy.availability == False:
            raise ValidationError("Copy is not available.")

        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)

        if user.block == True:
            raise ValidationError("The user is blocked.")

        copy.availability = False
        copy.save()

        term = self.calculate_prazo()
        serializer.save(user=user, copy=copy, term=term)

    def calculate_prazo(self):
        current_date = timezone.now()
        term = current_date + timedelta(days=7)

        if term.weekday() >= 5:
            term += timedelta(days=2)

        return term


class LoanDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_update(self, serializer):
        return serializer.save(
            copy_id=self.kwargs.get("pk"),
        )
