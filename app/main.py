from fastapi import Depends, FastAPI
from routers import test

app = FastAPI()
app.include_router(test.router)