"""Setup the router for the /test route"""
from fastapi import APIRouter,Body
from app.models.create_item import CreateItem
from app.models.create_item_response import CreateItemResponse
from pymongo import MongoClient

mdbc = MongoClient("mongodb://localhost:27017/")

router = APIRouter(
    prefix="/test",
    tags=["A test api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    """This is an example route, that returns a Hello World response"""
    return {"message": "Hello World!"}

@router.post("/")
async def create_item(item:CreateItem = Body(...), response_model=CreateItemResponse):
    """This method creates a new item entity and stores in MongoDb"""
    db = mdbc["test-database"]
    collection = db["test-collection"]
    result = collection.insert_one(jsonable_encoder(item))
    created_item =  collection.find_one({"_id": result.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_util.dumps(created_item,default=json_util.default))