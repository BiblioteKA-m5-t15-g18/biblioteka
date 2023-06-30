from django.db import models


class Book(models.Model):
    autor = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="books"
    )
