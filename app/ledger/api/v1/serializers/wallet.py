from rest_framework_json_api import serializers
from rest_framework_json_api.serializers import ValidationError
from ledger.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "label", "balance"]
        read_only_fields = ["balance"]


class WalletTransferSerializer(serializers.Serializer):
    source_wallet_id = serializers.IntegerField()
    destination_wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=32, decimal_places=18)

    class Meta:
        resource_name = "Wallet"

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs["source_wallet_id"] == attrs["destination_wallet_id"]:
            raise ValidationError("Cannot transfer to the same wallet")
        return attrs

    def validate_source_wallet_id(self, value):
        if not Wallet.objects.filter(pk=value).exists():
            raise ValidationError("From wallet does not exist")
        return value

    def validate_destination_wallet_id(self, value):
        if not Wallet.objects.filter(pk=value).exists():
            raise ValidationError("To wallet does not exist")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount must be greater than zero")
        return value


class WalletTransferResponseSerializer(serializers.Serializer):
    source_wallet = WalletSerializer()
    destination_wallet = WalletSerializer()

    class Meta:
        resource_name = "Wallet"
