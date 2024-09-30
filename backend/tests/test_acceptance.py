from http import HTTPStatus
from unittest.mock import ANY

from fastapi.testclient import TestClient


def test_can_fetch_investors(client: TestClient):
    response = client.get("/investors/")
    assert response.status_code == HTTPStatus.OK
    investors = response.json()
    assert len(investors["data"])
    for investor in investors["data"]:
        assert investor == {
            "address": ANY,
            "date_added": ANY,
            "id": ANY,
            "name": ANY,
            "total_commitment": ANY,
            "type": ANY,
        }


def test_can_paginate_investors(client: TestClient):
    response = client.get("/investors/?limit=2")
    assert response.status_code == HTTPStatus.OK
    first_page = response.json()
    assert not first_page["paging"]["previous"]
    next_page_url = first_page["paging"]["next"]
    next_page_response = client.get(next_page_url)
    second_page = next_page_response.json()

    assert first_page["data"] != second_page["data"]
    assert len(first_page["data"]) == len(second_page["data"]) == 2  # noqa: PLR2004


def test_can_fetch_asset_clases(client: TestClient):
    response_investor_3 = client.get("/investors/3/asset-classes/")
    assert response_investor_3.status_code == HTTPStatus.OK

    response_investor_2 = client.get("/investors/2/asset-classes/")
    assert response_investor_2.status_code == HTTPStatus.OK

    assert response_investor_2.json() != response_investor_3.json()


def test_can_filter_commitment_by_asset_classs(client: TestClient):
    response = client.get("/investors/3/commitment/?asset_class_id=1")
    assert response.status_code == HTTPStatus.OK

    all_asset_classes = {row["asset_class"] for row in response.json()["data"]}
    assert len(all_asset_classes) == 1
