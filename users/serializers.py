from rest_framework import serializers
from .models import User
from loan.serializer import LoanSerializer
from follow.serializer import FollowSerializer


class UserSerializer(serializers.ModelSerializer):
    loans = serializers.SerializerMethodField()
    following = FollowSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "password",
            "address",
            "is_staff",
            "block",
            "timeBlock",
            "loans",
            "following",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "block": {"read_only": True},
            "timeBlock": {"read_only": True},
        }

    def get_loans(self, obj):
        loans = obj.loans.order_by("-id")
        serializer = LoanSerializer(loans, many=True)
        return serializer.data

    def create(self, validated_data: dict) -> User:
        if validated_data.get("is_staff"):
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()

        return instance
