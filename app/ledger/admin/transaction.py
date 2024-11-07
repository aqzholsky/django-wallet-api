from django.contrib import admin

from ledger.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_select_related = ["wallet"]
    list_display = ["id", "wallet", "txid", "amount"]
    search_fields = ["txid", "wallet__label"]
    autocomplete_fields = ["wallet"]
    readonly_fields = ["created_at", "updated_at"]
