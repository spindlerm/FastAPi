"""Example pytest tests"""
from app.main import app
from fastapi.testclient import TestClient
from pydantic_mongo import ObjectIdField

client = TestClient(app)

def test_create():
    """Test the creation (post) and get for an item"""

    item_to_create = {
    "name": "joes Bloggs",
    "description": "This is joes item",
    "price": 10,
    "tax": 1.6
    }

    retrived_item = item_to_create

    response = client.post("/test", json=item_to_create)
    assert response.status_code == 201

   
    #Fetch th eitem with the return id to check it was created"
    id = ObjectIdField(response.json()["_id"])

    response = client.get(f"/test/{id}")
    assert response.status_code == 200

    #Add the returned id to the retrived_Item
    retrived_item["_id"] = id
    assert response.json() == retrived_item

def test_get_nonexistent_item():
    """When calling get with a non existant id, retrun 404 - Unprocessable body """
   
    #Fetch the item with valid non existant id
    id = "1111fa8fd3e0a099b5d3a813"

    response = client.get(f"/test/{ObjectIdField(id)}")
    assert response.status_code == 404
    assert response.json() == f"Item with id: {id} does not exist"

def test_get_with_invalid_id():
    """When calling get with a non existant id, return 422 - Unprocessable body """
   
    #Fetch the item with an invalid id
    id = ObjectIdField("invalidid")

    response = client.get(f"/test/{id}")
    assert response.status_code == 422


def test_delete_invalid_id():
    """When calling delete with a non existant id, return 422 - Unprocessable body """
   
    #Fetch the item with an invalid id
    id = ObjectIdField("invalidid")

    response = client.delete(f"/test/{id}")
    assert response.status_code == 422

   
def test_delete_nonexistent_item():
    """When calling delete with a non existant id, return 404 - Unprocessable body """
   
    #Fetch the item with valid non existant id
    id = "1111fa8fd3e0a099b5d3a813"

    response = client.delete(f"/test/{ObjectIdField(id)}")
    assert response.status_code == 404
    assert response.json() == f"Item with id: {id} does not exist"