from fastapi import FastAPI
import uvicorn
from data_interactor import *
from pydantic import BaseModel

class ContactBody(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

app = FastAPI()
connection = DataConnector()

def get_connection():
    connection = DataConnector()
    connection = connection.connecting()
    return connection

@app.get("/contacts")
def get_all_contacts():
    return connection.get_all_contacts()

@app.post("/contacts")
def create_new_contact(contact_data: ContactBody):
    new_id = connection.create_contact(contact_data.dict())
    return{
        "id": new_id
    }

@app.put("/contacts/{id}")
def update_contact_api(id):
    return connection.update_contact(id)

@app.delete("/contacts/{id}")
def del_api(id):
    return connection.delete_contact(id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)