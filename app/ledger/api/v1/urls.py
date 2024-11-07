from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet, WalletViewSet

app_name = "ledger-v1"

router = DefaultRouter()
router.register("wallets", WalletViewSet, basename="wallet")
router.register("transactions", TransactionViewSet, basename="transaction")
