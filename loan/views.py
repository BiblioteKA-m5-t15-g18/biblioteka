from rest_framework.generics import CreateAPIView
from .models import Loan
from .serializer import LoanSerializer
from rest_framework.permissions import (
    IsAdminUser,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from copies.models import Copy
from datetime import datetime, timedelta


class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.request.data.get("copy")
        copy = Copy.objects.get(id=copy_id)
        prazo = self.calculate_prazo()
        serializer.save(user=self.request.user, copy=copy, prazo=prazo)

    def calculate_prazo(self):
        current_date = datetime.now()
        prazo = current_date + timedelta(days=7)

        if prazo.weekday() >= 5:
            prazo += timedelta(days=2)

        return prazo
