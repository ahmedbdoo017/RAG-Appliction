from fastapi import FastAPI , APIRouter ,Depends
from helpers.config import get_settings, Settings


#create route object to use it in another files
base_router = APIRouter(
    prefix='/api/v1'
)

@base_router.get("/")

def welcome (app_settings : Settings = Depends(get_settings)):
    # get the name of app from the defined paramter in .env using setting class
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        'app name' : app_name,
        'app version' : app_version
    }
