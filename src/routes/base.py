from fastapi import FastAPI , APIRouter
import os

#create route object to use it in another files
base_router = APIRouter(
    prefix='/api/v1'
)

@base_router.get("/")

def welcome ():
    # get the name of app from the defined paramter in .env
    app_name = os.getenv("APP_NAME")
    app_version =os.getenv("APP_VERSION")
    return {
        'app name' : app_name,
        'app version' : app_version
    }
