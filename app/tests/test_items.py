"""This module contains PyTests for the Items FastApi endpoint"""
from fastapi import FastAPI, Response
from httpx import AsyncClient
from pydantic_mongo import ObjectIdField
import pytest


async def create_item(
    client: AsyncClient, item_to_create: dict, return_item: bool = False
) -> Response:
    """Helper method to create a new item in MongoDb"""
    if return_item is True:
        return await client.post("items/?return_item=True", json=item_to_create)

    return await client.post("items/", json=item_to_create)


async def delete_all_items(client: AsyncClient) -> None:
    """Fixture used to delete all ietms in the MongoDb"""
    response = await client.get("/items/?limit=1000")
    for item in response.json():
        response = await client.delete(f"/items/{item['_id']}?")


@pytest.mark.asyncio
# @pytest.mark.usefixtures("app")
async def test_create(app: FastAPI):
    """Test the creation (post) and get for an item"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    retrived_item = item_to_create

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.post("/items/", json=item_to_create)
        assert response.status_code == 201

        # Fetch the item with the return id to check it was created"
        item_id = ObjectIdField(response.json()["_id"])

        response = await async_client.get(f"/items/{item_id}")
        assert response.status_code == 200

        # Add the returned id to the retrived_Item
        retrived_item["_id"] = item_id
        assert response.json() == retrived_item


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_create_return_item_false(app):
    """Test the creation (post) and get for an item"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.post(
            "/items/?return_item=False", json=item_to_create
        )
        assert response.status_code == 201
        assert response.json() == {"_id": f'{response.json()["_id"]}'}


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_create_return_item_true(app):
    """Test the creation (post) and get for an item"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    item_created = item_to_create
    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await create_item(async_client, item_to_create, True)
        assert response.status_code == 201
        item_created["_id"] = response.json()["_id"]
        assert response.json() == item_created


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_create_with_missing_mandatory_fields(app):
    """Test the creation (post) with missing mandatory fields"""

    item_to_create = {
        "name": "joes Bloggs",
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await create_item(client=async_client, item_to_create=item_to_create)
        assert response.status_code == 422

        item_to_create = {"name": "joes Bloggs", "description": "descr"}

        response = await create_item(client=async_client, item_to_create=item_to_create)
        assert response.status_code == 422

        item_to_create = {"name": "joes Bloggs", "description": "descr", "price": 10}

        response = await create_item(client=async_client, item_to_create=item_to_create)
        assert response.status_code == 422

        item_to_create = {"name": "joes Bloggs", "description": "descr", "tax": 10.99}

        response = await create_item(client=async_client, item_to_create=item_to_create)
        assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_get_nonexistent_item(app):
    """When calling get with a non existant id, retrun 404 - Item not Found"""

    # Fetch the item with valid non existant id
    item_id = "1111fa8fd3e0a099b5d3a813"

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get(f"/items/{ObjectIdField(item_id)}")

    assert response.status_code == 404
    # assert response.json() == f"Item with id: {item_id} does not exist"


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_get_with_invalid_id(app):
    """When calling get with a non existant id, return 422 - Unprocessable body"""

    # Fetch the item with an invalid id
    item_id = ObjectIdField("invalidid")

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get(f"/items/{item_id}")
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_get_all_nolimit_no_skip(app):
    """When calling get with with no id, no limit or skip, should return all entries"""

    item_to_create = {
        "name": "Matt",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000/") as async_client:
        # Make sure there is at least 3 items existing in MongoDb
        await delete_all_items(async_client)
        for _ in range(0, 3):
            await create_item(async_client, item_to_create)

        response = await async_client.get("items/")
        assert response.status_code == 200

        item_list = list(response.json())
        assert len(item_list) == 3


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_get_all_with_limit(app):
    """When calling get with with no id, and a limit  should return (limit) no of items  entries"""

    item_to_create = {
        "name": "Fred",
        "description": "This is Fred item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        await delete_all_items(client=async_client)
        # Make sure there are 10 items existing in MongoDb
        for _ in range(0, 10):
            await create_item(client=async_client, item_to_create=item_to_create)

        # set limit to 5 items
        response = await async_client.get("/items/?limit=5")
        assert response.status_code == 200

        item_list = list(response.json())
        assert len(item_list) == 5


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_get_all_with_skip(app):
    """When calling get with just a skip value"""

    item_to_create = {
        "name": "Fred",
        "description": "This is Fred item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        await delete_all_items(client=async_client)
        # Make sure there are 10 items existing in MongoDb
        for _ in range(0, 10):
            await create_item(client=async_client, item_to_create=item_to_create)

        # set limit to 10 items and skip first 8, means should fetch 2
        response = await async_client.get("items/?limit=10&skip=8")
        assert response.status_code == 200

        item_list = list(response.json())
        assert len(item_list) == 2


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_get_all_with_skip_and_limit_paging(app):
    """When calling get with with no id, and a limit  should return (limit) no of items  entries"""

    item_to_create = {
        "name": "Fred",
        "description": "This is Fred item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        await delete_all_items(client=async_client)
        # Make sure there are 10 items existing in MongoDb
        for i in range(0, 10):
            item_to_create["price"] = i
            await create_item(client=async_client, item_to_create=item_to_create)

        # List itms 2 at a time, checking price
        for i in range(0, 5):
            response = await async_client.get(f"/items/?skip={i*2}&limit=2")
            assert response.status_code == 200
            item_list = list(response.json())
            assert len(item_list) == 2
            assert item_list[0]["price"] == (i * 2)
            assert item_list[1]["price"] == (i * 2) + 1


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_delete_invalid_id(app):
    """When calling delete with a non existant id, return 422 - Unprocessable body"""

    # Fetch the item with an invalid id
    item_id = ObjectIdField("invalidid")
    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.delete(f"/items/{item_id}")
        assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_delete_nonexistent_item(app):
    """When calling delete with a non existant id, return 404 - Item not Found"""

    # Fetch the item with valid non existant id
    item_id = "1111fa8fd3e0a099b5d3a813"

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.delete(f"/items/{ObjectIdField(item_id)}")
        assert response.status_code == 404
        assert response.json() == f"Item with id: {item_id} does not exist"


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_put_invalid_id(app):
    """When calling put with a non existant id, return 422 - Unprocessable body"""

    # Fetch the item with an invalid id
    item_id = ObjectIdField("invalidid")

    item_to_update = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.put(f"/items/{item_id}", json=item_to_update)
        assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_put_nonexistent_item(app):
    """When calling put with a non existant id, return 404 - Item not Found"""

    # Fetch the item with valid non existant id
    item_id = "1111fa8fd3e0a099b5d3a813"

    item_to_update = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.put(
            f"/items/{ObjectIdField(item_id)}", json=item_to_update
        )
        assert response.status_code == 404
        assert response.json() == f"Item with id: {item_id} does not exist"


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_put_with_valid_item_all_fields(app):
    """When calling put with a valid item (all fields), return 404 - Item not Found"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }
    item_to_update = item_to_create
    test_item = item_to_create
    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        response = await async_client.post("/items/", json=item_to_create)
        assert response.status_code == 201

        # Update the item with the return id to check it was created"
        item_id = ObjectIdField(response.json()["_id"])
        item_to_update["name"] = "updated name"
        response = await async_client.put(f"/items/{item_id}", json=item_to_update)
        assert response.status_code == 200

        # Fetch the updated item with the id and check it was updated"
        response = await async_client.get(f"/items/{ObjectIdField(item_id)}")
        assert response.status_code == 200
        test_item["name"] = "updated name"
        test_item["_id"] = item_id
        assert response.json() == item_to_create


@pytest.mark.asyncio
@pytest.mark.usefixtures("app")
async def test_put_with_valid_item_selected_fields(app):
    """When calling put with a valid item (selected fields), return 404 - Item not Found"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }
    item_to_update = {}
    test_item = item_to_create

    async with AsyncClient(app=app, base_url="http://localhost:8000/") as async_client:
        response = await async_client.post("/items/", json=item_to_create)
        assert response.status_code == 201

        # Update the item with the return id to check it was created"
        item_id = ObjectIdField(response.json()["_id"])
        item_to_update["name"] = "updated name"
        response = await async_client.put(f"/items/{item_id}", json=item_to_update)
        assert response.status_code == 200

        # Fetch the updated item with the id and check it was updated"
        response = await async_client.get(f"/items/{ObjectIdField(item_id)}")
        assert response.status_code == 200
        test_item["name"] = "updated name"
        test_item["_id"] = item_id
        assert response.json() == item_to_create
