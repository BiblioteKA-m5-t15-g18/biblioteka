from django.db import models

class Loan(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='loans')
    copias = models.ForeignKey("copies.Copy", on_delete=models.CASCADE, related_name='loans')
    date = models.DateTimeField()
    prazo = models.DateTimeField()
    devolvido = models.BooleanField(default=False)
