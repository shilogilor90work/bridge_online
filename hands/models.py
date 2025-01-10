from django.db import models


class Hand(models.Model):
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    update_at = models.DateTimeField('Updated', auto_now=True)
    cards = models.CharField(max_length=500)
    bids = models.CharField(max_length=1000)
    correct_answer = models.CharField(max_length=300)
    user_updated = models.CharField(max_length=100, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    optional_bids = models.CharField(max_length=300, blank=True, null=True)
    explanation = models.CharField(max_length=1000, blank=True, null=True)
    ns_vul = models.BooleanField(default=False)
    ew_vul = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not isinstance(self.metadata, dict):  # Enforce JSON type
            self.metadata = {}
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class Competition(models.Model):
    hands = models.ManyToManyField('Hand', related_name='competitions')
    users_input = models.JSONField(blank=True, null=True)  # JSON field for user input
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.id}, {self.hands}")
