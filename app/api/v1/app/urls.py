from django.urls import include, path

from ledger.api.v1.urls import router as ledger_router


app_name = "app"

urlpatterns = [
    path("ledger/", include(ledger_router.urls)),
]
