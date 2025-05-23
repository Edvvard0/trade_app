from django.db import models
from ads.models import Ad


STATUS_CHOICES = {
    "pending": "ожидает",
    "accepted": "принята",
    "rejected": "отклонена",
}


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="ad_sender")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="ad_receiver")
    comment = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES["pending"])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"

    def __str__(self):
        return f"Обмен: {self.ad_sender.title} на {self.ad_receiver.title} ({self.status})"