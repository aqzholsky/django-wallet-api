from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)

    def __str__(self):
        return self.label
