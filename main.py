from fastapi import FastAPI
# take an object from fastapi
app = FastAPI()

@app.get("/welcome")

def welcome ():
    return {
        "message" : "Hallo Hareedy"
    }
