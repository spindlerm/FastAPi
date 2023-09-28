"""This module is used to setup the FastAPI app and its routers"""
from fastapi import FastAPI
from app.routers import test
from pymongo import MongoClient
app = FastAPI()
app.include_router(test.router)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("mongodb://localhost:27017/")
    app.database = app.mongodb_client["test-database"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()