from decimal import Decimal

from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from ledger.models import Wallet


@pytest.mark.django_db
def test_get_wallet_list():
    client = APIClient()
    Wallet.objects.create(label="Wallet 1", balance=100)
    Wallet.objects.create(label="Wallet 2", balance=200)
    url = reverse("api:api-v1:app:wallet-list")
    response = client.get(url, format="vnd.api+json")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["label"] == "Wallet 1"
    assert response.data["results"][1]["label"] == "Wallet 2"


@pytest.mark.django_db
def test_retrieve_wallet():
    client = APIClient()
    wallet = Wallet.objects.create(label="Wallet 1", balance=100)
    url = reverse("api:api-v1:app:wallet-detail", args=[wallet.id])
    response = client.get(url, format="vnd.api+json")
    assert response.status_code == 200
    assert response.data["label"] == "Wallet 1"
    assert Decimal(response.data["balance"]) == 100


@pytest.mark.django_db
def test_transfer():
    client = APIClient()
    source_wallet = Wallet.objects.create(label="Source Wallet", balance=100)
    destination_wallet = Wallet.objects.create(label="Destination Wallet", balance=50)
    url = reverse("api:api-v1:app:wallet-transfer")
    data = {
        "data": {
            "type": "Wallet",
            "attributes": {
                "source_wallet_id": source_wallet.id,
                "destination_wallet_id": destination_wallet.id,
                "amount": "10",
            },
        }
    }
    response = client.post(url, data, format="vnd.api+json")
    print(response.data)
    assert response.status_code == 201
    source_wallet.refresh_from_db()
    destination_wallet.refresh_from_db()
    assert source_wallet.balance == 90
    assert destination_wallet.balance == 60
