from django.db import models

class Follow(models.Model):
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE, related_name='follows')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='following')
