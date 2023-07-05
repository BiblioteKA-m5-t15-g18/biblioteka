from .models import Book
from .serializer import BookSerializer
from copies.serializer import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadyOnly
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.permissions import (
    IsAdminUser,
)
from drf_spectacular.utils import extend_schema


class BookFilter(filters.FilterSet):
    autor = filters.CharFilter(field_name="autor", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = "__all__"


@extend_schema(tags=["Livros"])
class BookViewSet(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadyOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def perform_create(self, serializer):
        verify_book_existence = Book.objects.filter(
            title__iexact=serializer.validated_data.get("title")
        )

        if verify_book_existence.exists():
            book = verify_book_existence.first()
            copy_data = {"book": book.id, "user": self.request.user}
            new_copy = CopySerializer(data=copy_data)
            new_copy.is_valid(raise_exception=True)
            new_copy.save()

        serializer.save(user=self.request.user)


@extend_schema(tags=["Livros"])
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
