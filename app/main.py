"""This module is used to setup the FastAPI app and its routers"""
import os
from fastapi import FastAPI
import motor.motor_tornado
from mangum import Mangum
from app.routers import item


# AWS api gateway stage name
stage = os.getenv("ENVIRONMENT")

# Fix up the doc url, and openapi.json path to work with the stage name (if supplied)
root_path = f"/{stage}" if stage else "/"
doc_url = f"/{stage}/docs" if stage else "/docs"
openapi_url = f"/{stage}/openapi.json" if stage else "/openapi.json"


# This code block is my refactored main.py
def app_factory():
    """Helper factory method to create the FAstAPI App object"""
    myapp = FastAPI(openapi_url=openapi_url, docs_url=doc_url)
    if stage:
        myapp.include_router(item.router, prefix=root_path)
    else:
        myapp.include_router(item.router)

    return myapp


async def app_startup(my_app):
    """Startup event, connect to MongoDb"""
    #"mongodb://localhost:27017"#
    my_app.state.mongodb_client = motor.motor_tornado.MotorClient(
        "mongodb://tf_fast_api_admin:<insertYourPassword>@tf-fast-api.cluster-ca0oycycbugw.eu-west-2.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
    )
    my_app.state.database = my_app.state.mongodb_client["test-database"]
    my_app.state.collection = my_app.state.database["test-collection"]
    print("Connected to the MongoDB database!")


async def app_shutdown(my_app):
    """Shutdown event, disconnect from MongoDb"""
    my_app.state.mongodb_client.close()


app = app_factory()
handler = Mangum(app, lifespan="off")


@app.on_event("startup")
async def start_up():
    """Application startup event"""
    await app_startup(app)


@app.on_event("shutdown")
async def shutdown():
    """Application shutdown event"""
    await app_shutdown(app)
