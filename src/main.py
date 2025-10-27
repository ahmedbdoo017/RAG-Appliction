from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv('.env')
from routes import base
# take an object from fastapi
app = FastAPI()

app.include_router(base.base_router)