from django.db import models
from django.contrib.auth.models import User


class Loan(models.Model):
    # user = models.ForeignKey(
    #     "users.User", on_delete=models.CASCADE, related_name="loans"
    # )
    copias_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    prazo = models.DateTimeField()
    devolvido = models.BooleanField(default=False)
