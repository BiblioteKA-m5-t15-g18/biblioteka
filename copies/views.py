from .models import Copy
from .serializer import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class PermissionToRentView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        serializer.save(book=self.kwargs.get("book"))
