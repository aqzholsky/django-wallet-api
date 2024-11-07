from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from ledger.models import Transaction, Wallet


class TransactionInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        return super().get_queryset().order_by("-id")[:10]


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1
    fields = ["id", "txid", "amount"]
    show_change_link = True
    formset = TransactionInlineFormSet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["id", "label", "balance"]
    search_fields = ["label"]
    inlines = [TransactionInline]
    readonly_fields = ["balance", "created_at", "updated_at"]
