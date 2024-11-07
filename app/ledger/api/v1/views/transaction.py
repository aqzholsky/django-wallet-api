from django.db import transaction as db_transaction

from common.views import APIHandleExceptionMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework_json_api.filters import OrderingFilter
from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from ledger.api.v1.serializers.transaction import TransactionSerializer
from ledger.models import Transaction
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
    pagination_class = JsonApiPageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, filters.SearchFilter)
    search_fields = ("txid", "wallet__label")
    ordering_fields = ("id", "amount", "created_at", "updated_at")
    filterset_fields = ("wallet",)

    @db_transaction.atomic
    def perform_create(self, serializer):
        transaction = serializer.save()
        WalletService.create_cash_flow(transaction)
