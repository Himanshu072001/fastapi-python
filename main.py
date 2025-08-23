from fastapi import FastAPI
#from pydantic import BaseModel

app = FastAPI()



@app.get("/")
async def read_root():
    return {"data": "Welecome to FastAPI! This is a simple API built with FastAPI."}





