"""This module is used to setup the FastAPI app and its routers"""
from fastapi import FastAPI
import motor.motor_tornado
from app.routers import item


# This code block is my refactored main.py
def app_factory():
    """Helper factory method to create the FAstAPI App object"""
    myapp = FastAPI()
    myapp.include_router(item.router)
    return myapp


async def app_startup(my_app):
    """Startup event, connect to MongoDb"""
    my_app.state.mongodb_client = motor.motor_tornado.MotorClient(
        "mongodb://localhost:27017"
    )
    my_app.state.database = my_app.state.mongodb_client["test-database"]
    my_app.state.collection = my_app.state.database["test-collection"]
    print("Connected to the MongoDB database!")


async def app_shutdown(my_app):
    """Shutdown event, disconnect from MongoDb"""
    my_app.state.mongodb_client.close()


app = app_factory()


@app.on_event("startup")
async def start_up():
    """Application startup event"""
    await app_startup(app)


@app.on_event("shutdown")
async def shutdown():
    """Application shutdown event"""
    await app_shutdown(app)
