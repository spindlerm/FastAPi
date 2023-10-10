"""Setup the router for the /test route"""
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pydantic_mongo import ObjectIdField
from app.models.create_item import CreateItem
from app.models.update_item import UpdateItem
from app.models.item_response import ItemResponse


mdbc = MongoClient("mongodb://localhost:27017/")
data_base = mdbc["test-database"]
collection = data_base["test-collection"]

router = APIRouter(
    prefix="/items",
    tags=["Item api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{item_id}")
async def read_item(item_id: ObjectIdField) -> JSONResponse:
    """Called to get an Item"""

    item = collection.find_one({"_id": item_id})

    if item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Item with id: {item_id} does not exist",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(ItemResponse(**item)),
    )


@router.post("/")
async def create_item(
    item: CreateItem = Body(...), return_item: bool = False
) -> JSONResponse:
    """This method creates a new item entity and stores in MongoDb"""

    result = collection.insert_one(jsonable_encoder(item))

    if return_item is False:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder({"_id": str(result.inserted_id)}),
        )

    # Caller has requested that the inseted item be returned in the JSON response
    created_item = collection.find_one({"_id": result.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(ItemResponse(**created_item)),
    )


@router.delete("/{item_id}")
async def delete_item(item_id: ObjectIdField) -> JSONResponse:
    """This method deletes an item entity"""

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
    """This method implements put for an item entity"""
 
    items_to_update = {k: v for k, v in item.model_dump().items() if v is not None}

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
