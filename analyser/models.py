from django.db import models

class UserData(models.Model):
    keywords = models.TextField(null=False)