from fastapi import FastAPI
from fastapi import Body
#from pydantic import BaseModel

app = FastAPI()



@app.get("/")
async def read_root():
    return {"data": "Welecome to FastAPI! This is a simple API built with FastAPI."}


@app.get("/notes")
async def read_notes():
    return {"notes": ["Note 1", "Note 2", "Note 3"]}


@app.post("/create_note")
async def create_note(note: str, category: str):
    print(f"Creating note: {note} with category: {category}")
    return {"message": f"Note '{note}' with category '{category}' created successfully!"}

@app.post("/create_notes")
async def create_note(payload: dict = Body(...)):
    print(payload)
    return {"message": f"Note with params '{payload}' created successfully!"}
    


@app.post("/create_category")
async def create_category(category: str):
    print(f"Creating category: {category}")
    return {"message": f"Category '{category}' created successfully!"}  





