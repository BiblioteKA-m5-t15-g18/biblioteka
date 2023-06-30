from rest_framework import serializers
from .models import Book

# from users.models import User

# from users.serializer import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Book
        field = ["id", "autor", "title", "user_id"]

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
