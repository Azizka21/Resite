from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    people = models.TextField()  # Список
    people_array = models.JSONField(default=list)
    item_count = models.IntegerField(default=0)
    templates = models.JSONField(default=list)

    def __str__(self):
        return self.name