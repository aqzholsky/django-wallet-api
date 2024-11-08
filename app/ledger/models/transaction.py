from django.db import models

from common.models import TimestampMixin


class Transaction(TimestampMixin, models.Model):
    wallet = models.ForeignKey(
        "ledger.Wallet", on_delete=models.PROTECT, related_name="transactions"
    )
    txid = models.CharField(max_length=255, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
