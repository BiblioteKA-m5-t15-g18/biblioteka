from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    copies_total = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "autor", "title", "copies_total", "user_id"]
        extra_kwargs = {
            "copies_total": {"read_only": True},
            "copies": {"write_only": True},
        }

    def get_copies_total(self, obj) -> str:
        return obj.copies.count()

    def create(self, validated_data):
        title = validated_data.get("title")

        existing_book = Book.objects.filter(title__iexact=title).first()
        if existing_book:
            return existing_book

        if validated_data is not None:
            return Book.objects.create(**validated_data)
