"""This module is used to setup the FastAPI app and its routers"""
from fastapi import FastAPI
from app.routers import test

app = FastAPI()
app.include_router(test.router)