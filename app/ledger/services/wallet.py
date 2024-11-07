from decimal import Decimal
from uuid import uuid4

from django.db import transaction as db_transaction

from common.exceptions import UnprocessableEntityException

from ledger.models import Transaction, Wallet


class WalletService:
    @classmethod
    def create_cash_flow(cls, transaction: Transaction):
        wallet = Wallet.objects.select_for_update().get(pk=transaction.wallet_id)
        cls.check_balance(wallet, transaction.amount)
        wallet.balance += transaction.amount
        wallet.save(update_fields=["balance"])

    @classmethod
    def transfer(
        cls, source_wallet_id: int, destination_wallet_id: int, amount: Decimal
    ):
        with db_transaction.atomic():
            wallets_map = Wallet.objects.select_for_update().in_bulk(
                [source_wallet_id, destination_wallet_id]
            )
            source_wallet, destination_wallet = (
                wallets_map[source_wallet_id],
                wallets_map[destination_wallet_id],
            )
            cls.check_balance(source_wallet, amount)

            Transaction.objects.create(
                wallet=source_wallet,
                txid=uuid4().hex,
                amount=amount.copy_negate(),
            )
            Transaction.objects.create(
                wallet=destination_wallet,
                txid=uuid4().hex,
                amount=amount.copy_abs(),
            )
            source_wallet.balance -= amount
            destination_wallet.balance += amount
            source_wallet.save(update_fields=["balance"])
            destination_wallet.save(update_fields=["balance"])

        return source_wallet, destination_wallet

    @staticmethod
    def check_balance(wallet: Wallet, amount: Decimal):
        if amount < 0 and wallet.balance < amount.copy_abs():
            raise UnprocessableEntityException("Insufficient funds")
