from django.db import models

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    copias = models.ForeignKey(Copies, on_delete=models.CASCADE)
    date = models.DateTimeField()
    prazo = models.DateTimeField()
    devolvido = models.BooleanField(default=False)
