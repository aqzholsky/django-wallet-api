from ledger.models import Transaction
from rest_framework import viewsets, mixins
from ledger.api.v1.serializers.transaction import TransactionSerializer
from django.db import transaction as db_transaction
from common.views import APIHandleExceptionMixin
from ledger.services.wallet import WalletService


class TransactionViewSet(
    APIHandleExceptionMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Transaction.objects.all().select_related("wallet")
    serializer_class = TransactionSerializer

    @db_transaction.atomic
    def perform_create(self, serializer):
        transaction = serializer.save()
        WalletService.create_cash_flow(transaction)
