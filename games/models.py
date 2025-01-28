from django.db import models


class Game(models.Model):
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    update_at = models.DateTimeField('Updated', auto_now=True)
    n_cards_s = models.CharField(max_length=30)
    n_cards_h = models.CharField(max_length=30)
    n_cards_d = models.CharField(max_length=30)
    n_cards_c = models.CharField(max_length=30)
    e_cards_s = models.CharField(max_length=30)
    e_cards_h = models.CharField(max_length=30)
    e_cards_d = models.CharField(max_length=30)
    e_cards_c = models.CharField(max_length=30)
    s_cards_s = models.CharField(max_length=30)
    s_cards_h = models.CharField(max_length=30)
    s_cards_d = models.CharField(max_length=30)
    s_cards_c = models.CharField(max_length=30)
    w_cards_s = models.CharField(max_length=30)
    w_cards_h = models.CharField(max_length=30)
    w_cards_d = models.CharField(max_length=30)
    w_cards_c = models.CharField(max_length=30)
    ns_vul = models.BooleanField(default=False)
    ew_vul = models.BooleanField(default=False)
    dealer = models.CharField(max_length=10)
    bids = models.JSONField(default=list, blank=True)  # {"start": "n", "bids": ["Pass", "1C", "Pass", "Pass", "Pass"]}
    round_1 = models.JSONField(default=dict, blank=True)  # who starts and 4 cards : {"start": "n", "n": "5C", "e": "6C", "s": "7C", "w": "8C"}
    round_2 = models.JSONField(default=dict, blank=True)
    round_3 = models.JSONField(default=dict, blank=True)
    round_4 = models.JSONField(default=dict, blank=True)
    round_5 = models.JSONField(default=dict, blank=True)
    round_6 = models.JSONField(default=dict, blank=True)
    round_7 = models.JSONField(default=dict, blank=True)
    round_8 = models.JSONField(default=dict, blank=True)
    round_9 = models.JSONField(default=dict, blank=True)
    round_10 = models.JSONField(default=dict, blank=True)
    round_11 = models.JSONField(default=dict, blank=True)
    round_12 = models.JSONField(default=dict, blank=True)
    round_13 = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    explanation = models.CharField(max_length=2000, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not isinstance(self.metadata, dict):  # Enforce JSON type
            self.metadata = {}
        if not isinstance(self.bids, list):  # Enforce JSON type
            self.bids = []
        for i in range(1, 14):
            attr_name = f"round_{i}"
            value = getattr(self, attr_name, None)
            if not isinstance(value, dict):  # Enforce JSON type
                setattr(self, attr_name, {})
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
