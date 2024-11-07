from decimal import Decimal

import pytest

from ledger.models import Transaction, Wallet
from ledger.services.wallet import WalletService


@pytest.mark.django_db
def test_create_cash_flow():
    wallet = Wallet.objects.create(label="Test Wallet", balance=100)
    transaction = Transaction.objects.create(wallet=wallet, amount=50)
    WalletService.create_cash_flow(transaction)
    wallet.refresh_from_db()
    assert wallet.balance == 150


@pytest.mark.django_db
def test_transfer():
    source_wallet = Wallet.objects.create(label="Source Wallet", balance=100)
    destination_wallet = Wallet.objects.create(label="Destination Wallet", balance=50)
    WalletService.transfer(source_wallet.id, destination_wallet.id, Decimal(20))
    source_wallet.refresh_from_db()
    destination_wallet.refresh_from_db()
    assert source_wallet.balance == 80
    assert destination_wallet.balance == 70
