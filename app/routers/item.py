"""Setup the router for the /test route"""
from fastapi import APIRouter, Body, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic_mongo import ObjectIdField
from bson import ObjectId
from app.models.create_item import CreateItem
from app.models.update_item import UpdateItem
from app.models.item_response import ItemResponse

# pylint: disable=W0108
router = APIRouter(
    prefix="/items",
    tags=["Item api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{item_id}")
async def read_item(item_id: ObjectIdField, request: Request) -> JSONResponse:
    """Called to get an Item using its id"""

    item = await request.app.state.collection.find_one({"_id": item_id})

    if item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Item with id: {item_id} does not exist",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(ItemResponse(**item)),
    )


@router.get("/")
async def read_all_items(
    request: Request, limit: int = 5, skip: int = 0, response_model=list[ItemResponse]
) -> JSONResponse:
    # pylint: disable=unused-argument
    """Called to return a list of items, this method is pagable and you can limit the results too"""
    return_list = []
    cursor = request.app.state.collection.find({}).skip(skip).limit(limit)
    async for item in cursor:
        return_list.append(item)
    # return_list = await cursor.to_list(length=limit)

    return jsonable_encoder(
        return_list,
        custom_encoder={ObjectId: lambda oid: str(oid)},
    )


@router.post("/")
async def create_item(
    request: Request, item: CreateItem = Body(...), return_item: bool = False
) -> JSONResponse:
    """This method creates a new item"""

    result = await request.app.state.collection.insert_one(jsonable_encoder(item))

    if return_item is False:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder({"_id": str(result.inserted_id)}),
        )

    # Caller has requested that the inseted item be returned in the JSON response
    created_item = await request.app.state.collection.find_one(
        {"_id": result.inserted_id}
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(ItemResponse(**created_item)),
    )


@router.delete("/{item_id}")
async def delete_item(request: Request, item_id: ObjectIdField) -> JSONResponse:
    """This method deletes an item"""

    result = await request.app.state.collection.delete_one({"_id": item_id})

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
    request: Request, item_id: ObjectIdField, item: UpdateItem = Body(...)
) -> JSONResponse:
    """This method updates an existing item"""

    items_to_update = {k: v for k, v in item.model_dump().items() if v is not None}

    if len(items_to_update) >= 1:
        update_result = await request.app.state.collection.update_one(
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
