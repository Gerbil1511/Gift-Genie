from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.item_name