from django.db import models
from django.contrib.auth.models import User
from wishlist.models import WishlistItem

class Planner(models.Model):
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wishlist = models.ForeignKey(WishlistItem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.event_name

