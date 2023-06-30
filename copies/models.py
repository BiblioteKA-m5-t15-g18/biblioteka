from django.db import models

class Copy(models.Model):
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE, related_name='copies')
    loan = models.CharField(max_length=50, null=True)
    disponibilidade = models.BooleanField(default=True)
