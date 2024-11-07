from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from ledger.models import Transaction, Wallet


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def wallet(db):
    return Wallet.objects.create(label="Test Wallet")


@pytest.fixture
def transaction(wallet):
    return Transaction.objects.create(
        wallet=wallet,
        amount=100,
        txid="txid",
    )


@pytest.mark.django_db
def test_list_transactions(api_client, wallet, transaction):
    url = reverse("api:api-v1:app:transaction-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_retrieve_transaction(api_client, wallet, transaction):
    url = reverse("api:api-v1:app:transaction-detail", args=[transaction.id])
    response = api_client.get(url)
    assert response.status_code == 200
