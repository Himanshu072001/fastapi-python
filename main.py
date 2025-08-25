from typing import Optional
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the request body
class Note(BaseModel):
    note: str
    category: str  
    bookmarked: bool = False # Optional field with a default value
    saved: Optional[bool] = None # Optional field without a default value 


@app.get("/")
async def read_root():
    return {"data": "Welecome to FastAPI! This is a simple API built with FastAPI."}


@app.get("/notes")
async def read_notes():
    return {"notes": ["Note 1", "Note 2", "Note 3"]}


# Method 1: Using path parameters
@app.post("/create_note")
async def create_note(note: str, category: str):
    print(f"Creating note: {note} with category: {category}")
    return {"message": f"Note '{note}' with category '{category}' created successfully!"}

# Method 2: Using request body
@app.post("/create_notes")
async def create_note(payload: dict = Body(...)):
    print(payload)
    return {"message": f"Note with params '{payload}' created successfully!"}

@app.post("/create_notes_model")
async def create_note(note: Note):
    print(note)
    print(note.dict())
    return {"message": f"Note '{note.note}' with category '{note.category}' '{note.bookmarked}' {note.saved} created successfully!"}
    

@app.post("/create_category")
async def create_category(category: str):
    print(f"Creating category: {category}")
    return {"message": f"Category '{category}' created successfully!"}  





