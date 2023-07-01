from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "date", "prazo", "devolvido"]
        read_only_fields = ["id", "date", "prazo", "devolvido", "prazo"]

    def create(self, validated_data):
        return Loan.objects.create(**validated_data)
