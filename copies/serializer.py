from rest_framework import serializers
from .models import Copy
from book.serializer import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    def create(self, validated_data):
        return Copy.objects.create(**validated_data)

    class Meta:
        model = Copy
        filds = "__all__"
