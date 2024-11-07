from rest_framework_json_api import serializers
from ledger.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount"]
        read_only_fields = ["id"]
