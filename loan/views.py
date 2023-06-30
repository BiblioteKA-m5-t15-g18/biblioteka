from rest_framework.generics import CreateAPIView
from .models import Loan
from .serializer import LoanSerializer


class LoanView(CreateAPIView):

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        user = get_object_or_404(User,id=user_id)
        copy_id = self.request.data.get('user_id')
        copy = User.objects.get(id=user_id)
        serializer.save(user=user, copy=copy)
