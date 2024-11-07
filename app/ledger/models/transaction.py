from django.db import models


class Transaction(models.Model):
    wallet = models.ForeignKey(
        "ledger.Wallet", on_delete=models.PROTECT, related_name="transactions"
    )
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
