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
        read_only_fields = ["id", "date", "returned", "term"]

    def create(self, validated_data):
        return Loan.objects.create(**validated_data)

    def update(self, instance: Loan, validated_data: dict) -> Loan:
        copy = Copy.objects.get(id=validated_data["copy_id"])
        copy.availability = True
        copy.save()

        loan = Loan.objects.get(id=copy.loan)
        loan.returned = True
        loan.save()

        current_date = timezone.now()
        print(current_date > loan.term)

        if current_date > loan.term:
            user = User.objects.get(id=loan.user_id)
            user.block = True

            prazo = current_date + timedelta(days=7)
            user.timeBlock = prazo
            user.save()

        return loan
