"""Setup the router for the /test route"""
from fastapi import APIRouter


router = APIRouter(
    prefix="/test",
    tags=["A test api"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_test():
    """This is an example route, that returns a Hello World response"""
    return {"message: Hello World!"}
