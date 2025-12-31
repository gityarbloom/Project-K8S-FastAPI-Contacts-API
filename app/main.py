from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
from data.data_interactor import *

app = FastAPI()

class Contact(BaseModel):
    fisrt_name : str
    last_name: str 
    phone_num: str

def get_connection():
    try:
        connection = MongodbConnect()
    except Exception as e:
        raise HTTPException(
                status_code=400, detail=f"Error by creating connection:\n{e}"
            )
    return connection


@app.get("/contacts")
def get_all_contacts():    
    acess = get_connection()
    all_contacts = acess.get_all()
    return all_contacts
    
@app.post("/contacts")
def create_contat(contact_data: Contact):
    acess = get_connection()
    try:
        new_contact = contact_data.model_dump()
        creating =  acess.create_new_contact(new_contact)
    except:
        return "Contact creation was failed"
    return f"Contact creation successful! The new contact ID is: {creating}"

@app.put("/contacts/{id}")
def update_contact(id: str, contact_data: Contact):
    acess = get_connection()
    try:
        new_contact = contact_data.model_dump()
        acess.update(id, new_contact)
    except:
        return "The update was failed"
    return "The update was successful"

@app.delete("/contacts/{id}")
def delete_contact(id: str):
    acess = get_connection()
    return acess.delete_one_contact(id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)