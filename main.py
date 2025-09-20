from fastapi import HTTPException
from fastapi import status, Response
from typing import Optional
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Define a Pydantic model for the request body
class Note(BaseModel):
    note: str
    category: str  
    bookmarked: bool = False # Optional field with a default value
    saved: Optional[bool] = None # Optional field without a default value 

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break;
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)   


# Simple GET endpoint to check if the API is running
@app.get("/")
async def read_root():
    return {"data": "Welecome to FastAPI! This is a simple API built with FastAPI."}

# Simple GET endpoint to fetch notes
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

# Method 3: Using Pydantic model
@app.post("/create_notes_model")
async def create_note(note: Note):
    print(note)
    print(note.dict())
    return {"message": f"Note '{note.note}' with category '{note.category}' '{note.bookmarked}' {note.saved} created successfully!"}
    
# Method 4: Using only one parameter in the body
@app.post("/create_category")
async def create_category(category: str):
    print(f"Creating category: {category}")
    return {"message": f"Category '{category}' created successfully!"}  


# CRUD Operations

# In-memory storage for notes
notes_db = [{"id": 1, "note": "Sample Note", "category": "General", "bookmarked": False, "saved": None},
            {"id": 2, "note": "Another Note", "category": "Work", "bookmarked": True, "saved": True}]

# Create a new note
#satus code 201 means resource created successfully & status code will be shown in the postman response
@app.post("/notes/create", status_code=status.HTTP_201_CREATED)
async def create_note_db(note: Note):
    new_id = len(notes_db) + 1
    new_note = note.dict()
    new_note["id"] = new_id
    notes_db.append(new_note)
    print(notes_db)
    return {"message": "Note created successfully", "note": new_note}       

# Read all notes
@app.get("/notes/all")
async def get_all_notes():
    return {"notes": notes_db}  

# Read a specific note by ID
@app.get("/notes/{id}")
async def get_note_by_id(id: int):
    for note in notes_db:
        if note["id"] == id:
            return {"note": note}
    raise HTTPException(status_code=404, detail= f"note with note_Id = {id} not found")
   # return {"error": "Note not found"}


# Update a note by ID
@app.put("/notes/update/{id}")
async def update_note(id: int, updated_note: Note):
    for index, note in enumerate(notes_db):
        if note["id"] == id:
            notes_db[index] = updated_note.dict()
            notes_db[index]["id"] = id
            return {"message": "Note updated successfully", "note": notes_db[index]}
    return {"error": "Note not found"}  

# Delete a note by ID
@app.delete("/notes/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: int):
    for index, note in enumerate(notes_db):
        if note["id"] == id:
            deleted_note = notes_db.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            #return {"message": "Note deleted successfully", "note": deleted_note}
    raise HTTPException(status_code=404, detail= f"note with note_Id = {id} not found")
    # return {"error": "Note not found"}


