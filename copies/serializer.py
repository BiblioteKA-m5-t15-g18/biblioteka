from rest_framework import serializers
from django.shortcuts import get_object_or_404
from book.models import Book
from .models import Copy


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = "__all__"
        extra_kwargs = {
            "book_id": {"write_only": True},
            "available": {"write_only": True},
        }

    def create(self, validated_data):
        return Copy.objects.create(**validated_data)
