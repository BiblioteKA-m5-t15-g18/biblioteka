from .models import Book
from .serializer import BookSerializer
from copies.serializer import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadyOnly
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAdminUser,
)
from users.permissions import IsAccountOnwer


class BookView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadyOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadyOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["autor", "title"]
    search_fields = ["autor", "title"]

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


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAccountOnwer]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
