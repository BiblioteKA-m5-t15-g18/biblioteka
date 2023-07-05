from django.db import models

class Loan(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='loans')
    copy = models.ForeignKey("copies.Copy", on_delete=models.CASCADE, related_name='loans')
    date = models.DateTimeField(auto_now_add=True)
    term = models.DateTimeField()
    returned = models.BooleanField(default=False, null=True)
