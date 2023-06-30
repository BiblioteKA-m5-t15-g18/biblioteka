from django.db import models

class Copies(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    disponibilidade = models.BooleanField(default=True)
