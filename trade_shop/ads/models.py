from django.db import models
from django.contrib.auth.models import User


CONDITION_CHOICES = {
    "new": "новый",
    "used": "б/у"
}

CATEGORY_CHOICES = {
    "cars": "машины",
    "house": "дома",
    "hobby": "хобби",
    "other": "другое",
}


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES)
    condition = models.CharField(choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)
