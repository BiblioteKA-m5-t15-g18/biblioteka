from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ("id", "user", "copias_id", "date", "prazo", "devolvido")
