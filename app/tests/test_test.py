"""Example pytest tests"""
from fastapi import Response
from fastapi.testclient import TestClient
from pydantic_mongo import ObjectIdField
from app.main import app

client = TestClient(app)


def create_item(item_to_create: dict, return_item: bool = False) -> Response:
    """Helper method to create a new item in MongoDb"""
    if return_item is True:
        return client.post("/items?return_item=True", json=item_to_create)

    return client.post("/items", json=item_to_create)


def test_create():
    """Test the creation (post) and get for an item"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    retrived_item = item_to_create

    response = client.post("/items", json=item_to_create)
    assert response.status_code == 201

    # Fetch the item with the return id to check it was created"
    item_id = ObjectIdField(response.json()["_id"])

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

    # Add the returned id to the retrived_Item
    retrived_item["_id"] = item_id
    assert response.json() == retrived_item


def test_create_return_item_false():
    """Test the creation (post) and get for an item"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    response = client.post("/items?return_item=False", json=item_to_create)
    assert response.status_code == 201
    assert response.json() == {"_id": f'{response.json()["_id"]}'}


def test_create_return_item_true():
    """Test the creation (post) and get for an item"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    item_created = item_to_create

    response = create_item(item_to_create, True)
    assert response.status_code == 201
    item_created["_id"] = response.json()["_id"]
    assert response.json() == item_created


def test_create_with_missing_mandatory_fields():
    """Test the creation (post) with missing mandatory fields"""

    item_to_create = {
        "name": "joes Bloggs",
    }

    response = create_item(item_to_create)
    assert response.status_code == 422

    item_to_create = {"name": "joes Bloggs", "description": "descr"}

    response = create_item(item_to_create)
    assert response.status_code == 422

    item_to_create = {"name": "joes Bloggs", "description": "descr", "price": 10}

    response = create_item(item_to_create)
    assert response.status_code == 422

    item_to_create = {"name": "joes Bloggs", "description": "descr", "tax": 10.99}

    response = create_item(item_to_create)
    assert response.status_code == 422


def test_get_nonexistent_item():
    """When calling get with a non existant id, retrun 404 - Item not Found"""

    # Fetch the item with valid non existant id
    item_id = "1111fa8fd3e0a099b5d3a813"

    response = client.get(f"/items/{ObjectIdField(item_id)}")
    assert response.status_code == 404
    assert response.json() == f"Item with id: {item_id} does not exist"


def test_get_with_invalid_id():
    """When calling get with a non existant id, return 422 - Unprocessable body"""

    # Fetch the item with an invalid id
    item_id = ObjectIdField("invalidid")

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 422


def test_get_all():
    """When calling get with with no id, should return all entries"""

    item_to_create = {
        "name": "Matt",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    # Make sure there is at least 3 items existing in MongoDb
    create_item(item_to_create)
    create_item(item_to_create)
    create_item(item_to_create)

    response = client.get("/items")
    assert response.status_code == 200

    item_list = list(response.json())
    assert len(item_list) >= 3


def test_delete_invalid_id():
    """When calling delete with a non existant id, return 422 - Unprocessable body"""

    # Fetch the item with an invalid id
    item_id = ObjectIdField("invalidid")

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 422


def test_delete_nonexistent_item():
    """When calling delete with a non existant id, return 404 - Item not Found"""

    # Fetch the item with valid non existant id
    item_id = "1111fa8fd3e0a099b5d3a813"

    response = client.delete(f"/items/{ObjectIdField(item_id)}")
    assert response.status_code == 404
    assert response.json() == f"Item with id: {item_id} does not exist"


def test_put_invalid_id():
    """When calling put with a non existant id, return 422 - Unprocessable body"""

    # Fetch the item with an invalid id
    item_id = ObjectIdField("invalidid")

    item_to_update = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    response = client.put(f"/items/{item_id}", json=item_to_update)
    assert response.status_code == 422


def test_put_nonexistent_item():
    """When calling put with a non existant id, return 404 - Item not Found"""

    # Fetch the item with valid non existant id
    item_id = "1111fa8fd3e0a099b5d3a813"

    item_to_update = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }

    response = client.put(f"/items/{ObjectIdField(item_id)}", json=item_to_update)
    assert response.status_code == 404
    assert response.json() == f"Item with id: {item_id} does not exist"


def test_put_with_valid_item_all_fields():
    """When calling put with a valid item (all fields), return 404 - Item not Found"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }
    item_to_update = item_to_create
    test_item = item_to_create
    response = client.post("/items", json=item_to_create)
    assert response.status_code == 201

    # Update the item with the return id to check it was created"
    item_id = ObjectIdField(response.json()["_id"])
    item_to_update["name"] = "updated name"
    response = client.put(f"/items/{item_id}", json=item_to_update)
    assert response.status_code == 200

    # Fetch the updated item with the id and check it was updated"
    response = client.get(f"/items/{ObjectIdField(item_id)}")
    assert response.status_code == 200
    test_item["name"] = "updated name"
    test_item["_id"] = item_id
    assert response.json() == item_to_create


def test_put_with_valid_item_selected_fields():
    """When calling put with a valid item (selected fields), return 404 - Item not Found"""

    item_to_create = {
        "name": "joes Bloggs",
        "description": "This is joes item",
        "price": 10,
        "tax": 1.6,
    }
    item_to_update = {}
    test_item = item_to_create
    response = client.post("/items", json=item_to_create)
    assert response.status_code == 201

    # Update the item with the return id to check it was created"
    item_id = ObjectIdField(response.json()["_id"])
    item_to_update["name"] = "updated name"
    response = client.put(f"/items/{item_id}", json=item_to_update)
    assert response.status_code == 200

    # Fetch the updated item with the id and check it was updated"
    response = client.get(f"/items/{ObjectIdField(item_id)}")
    assert response.status_code == 200
    test_item["name"] = "updated name"
    test_item["_id"] = item_id
    assert response.json() == item_to_create
