from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_json_api.filters import OrderingFilter
from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from ledger.api.v1.serializers import WalletSerializer, WalletTransferResponseSerializer, WalletTransferSerializer
from ledger.models import Wallet
from ledger.services.wallet import WalletService


class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Wallet.objects.all().prefetch_related("transactions")
    serializer_class = WalletSerializer
    pagination_class = JsonApiPageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, filters.SearchFilter)
    search_fields = ("label",)
    ordering_fields = ("id", "balance", "created_at", "updated_at")
    filterset_fields = ("label",)

    def get_serializer_class(self):
        if self.action == "transfer":
            return WalletTransferSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Transfer money between wallets",
        request=WalletTransferSerializer,
        responses=WalletTransferResponseSerializer,
    )
    @action(methods=["post"], detail=False)
    def transfer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_wallet, destination_wallet = WalletService.transfer(
            serializer.validated_data["source_wallet_id"],
            serializer.validated_data["destination_wallet_id"],
            serializer.validated_data["amount"],
        )

        serializer = WalletTransferResponseSerializer(
            {
                "source_wallet": source_wallet,
                "destination_wallet": destination_wallet,
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
