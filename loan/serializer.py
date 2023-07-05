from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import Loan
from users.models import User
from copies.models import Copy


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "date", "term", "returned"]
        read_only_fields = ["id", "date", "term", "returned", "term"]

    def create(self, validated_data):
        return Loan.objects.create(**validated_data)

    def update(self, instance: Loan, validated_data: dict) -> Loan:
        loan = Loan.objects.get(id=validated_data["loan_id"])
        loan.returned = True
        loan.save()

        copy = Copy.objects.get(id=validated_data["copy_id"])
        copy.available = True
        copy.save()

        if validated_data["block"]:
            user = User.objects.get(id=validated_data["user_id"])

            current_date = timezone.now()
            prazo = current_date + timedelta(days=7)
            user.timeBlock = prazo
            user.save()

        return loan
