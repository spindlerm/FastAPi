"""This module is used to setup the FastAPI app and its routers"""
from fastapi import FastAPI
from pymongo import MongoClient
from app.routers import test


app = FastAPI()
app.include_router(test.router)


@app.on_event("startup")
def startup_db_client():
    """Startup event, connect to MongoDb"""
    app.mongodb_client = MongoClient("mongodb://localhost:27017/")
    app.database = app.mongodb_client["test-database"]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    """Shutdown event, disconnect from MongoDb"""
    app.mongodb_client.close()
