"""Setup the router for the /test route"""
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from app.models.create_item import CreateItem
from app.models.create_item_response import CreateItemResponse
from pydantic_mongo import ObjectIdField

mdbc = MongoClient("mongodb://localhost:27017/")

router = APIRouter(
    prefix="/test",
    tags=["A test api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}") 
async def read_test(id: ObjectIdField) -> JSONResponse:
    """This is an example route, that returns a Hello World response"""
    data_base = mdbc["test-database"]
    collection = data_base["test-collection"]
    item = collection.find_one({"_id": id})

    if item == None:
             return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=f"Item with id: {id} does not exist")
    else:
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


@router.delete("/{id}")
async def delete_item(id: ObjectIdField) -> JSONResponse:
    """This method delete an  item entity"""
    data_base = mdbc["test-database"]
    collection = data_base["test-collection"]
    result = collection.delete_one({"_id": id})
  
    if result.acknowledged & result.deleted_count ==1:
             return JSONResponse(status_code=status.HTTP_200_OK,
                            content=f"Item with id: {id} deleted")
    else:
         return JSONResponse(
         status_code=status.HTTP_404_NOT_FOUND,
         content=f"Item with id: {id} does not exist")