from rest_framework import generics
from .models import Loan
from .serializer import LoanSerializer
from copies.serializer import CopySerializer
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
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404


@extend_schema(tags=["Empréstimos"])
class LoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.request.data.get("copy")
        copy = Copy.objects.get(id=copy_id)

        if copy.available == False:
            raise ValidationError("Copy is not available.")

        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)

        if user.block == True:
            raise ValidationError("The user is blocked.")

        copy.available = False
        copy.save()

        term = self.calculate_prazo()
        loan = serializer.save(user=user, copy=copy, term=term)

        copy.loan = loan.id
        copy.save()

    def calculate_prazo(self):
        current_date = timezone.now()
        prazo = current_date + timedelta(days=7)

        if prazo.weekday() >= 5:
            prazo += timedelta(days=2)

        return prazo


@extend_schema(tags=["Empréstimos"])
class LoanDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_update(self, serializer):
        copy = get_object_or_404(Copy, pk=self.kwargs["pk"])
        try:
            loan = Loan.objects.get(id=copy.loan)
        except:
            raise ValidationError("This copy is not on loan")

        if loan.returned == True:
            raise ValidationError("This loan has already been returned.")

        copy.available = True
        copy.loan = None
        loan.returned = True

        loan.save()
        copy.save()
