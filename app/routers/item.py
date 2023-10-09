"""Setup the router for the /test route"""
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pydantic_mongo import ObjectIdField
from app.models.create_item import CreateItem
from app.models.update_item import UpdateItem
from app.models.create_item_response import CreateItemResponse


mdbc = MongoClient("mongodb://localhost:27017/")

router = APIRouter(
    prefix="/items",
    tags=["Item api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{item_id}")
async def read_test(item_id: ObjectIdField) -> JSONResponse:
    """Called to get an Item"""
    data_base = mdbc["test-database"]
    collection = data_base["test-collection"]
    item = collection.find_one({"_id": item_id})

    if item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Item with id: {item_id} does not exist",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(CreateItemResponse(**item)),
    )


@router.post("/")
async def create_item(item: CreateItem = Body(...)) -> JSONResponse:
    """This method creates a new item entity and stores in MongoDb"""
    data_base = mdbc["test-database"]
    collection = data_base["test-collection"]
    result = collection.insert_one(jsonable_encoder(item))
    created_item = collection.find_one({"_id": result.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(CreateItemResponse(**created_item)),
    )


@router.delete("/{item_id}")
async def delete_item(item_id: ObjectIdField) -> JSONResponse:
    """This method delete an  item entity"""
    data_base = mdbc["test-database"]
    collection = data_base["test-collection"]
    result = collection.delete_one({"_id": item_id})

    if result.acknowledged & result.deleted_count == 1:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=f"Item with id: {item_id} deleted"
        )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=f"Item with id: {item_id} does not exist",
    )


@router.put("/{item_id}")
async def put_item(
    item_id: ObjectIdField, item: UpdateItem = Body(...)
) -> JSONResponse:
    """This method update an item entity"""
    data_base = mdbc["test-database"]
    collection = data_base["test-collection"]

    items_to_update = {k: v for k, v in item.dict().items() if v is not None}

    if len(items_to_update) >= 1:
        update_result = collection.update_one(
            {"_id": item_id}, {"$set": items_to_update}
        )

        if update_result.matched_count == 1:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Item with id: {item_id} updated",
            )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Item with id: {item_id} does not exist",
        )
