from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["A test api"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_test():
    return {"message: Hello world!"}
