from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
config = {
            "host": os.getenv("MONGO_HOST"),
            "port": os.getenv("MONGO_PORT"),
            "db_name": os.getenv("MONGO_DB"),
        }

class Contact:
    def __init__(self, first_name:str, last_name:str, phone_number:str, id:int|None = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def to_dict(self):
        return self.__dict__



class MongodbConnect:
    def __init__(self, db_host:str=config["host"], db_port:int=int(config["port"])):
        self.client = MongoClient(db_host, db_port)
    
    def db_acess(self, db_name:str):
        self.db = self.client[db_name]
        return self.db
    
    def coll_aacess(self, db_name:str=config["db_name"], coll_name:str="my_contacts"):
        self.db = self.db_acess(db_name)
        self.collection = self.db[coll_name]
        return self.collection

    def get_all(self):
        contact_list = []
        connect_to_coll = self.coll_aacess()
        all_contacts = connect_to_coll.find()
        for doc in all_contacts:
            doc["_id"] = str(doc["_id"])
            contact_list.append(doc)
        return contact_list
    
    def create_new_contact(self, contact_data: dict):
        connect_to_coll = self.coll_aacess()
        result = connect_to_coll.insert_one(contact_data)
        return str(result.inserted_id)
    
    def update(self, id, new_contact:dict):
        coll = self.coll_aacess()
        try:
            coll.update_one({"_id": ObjectId(id)}, {"$set": new_contact})
        except:
            return False
        return True

    def delete_one_contact(self, id:str):
        coll = self.coll_aacess()
        try:
            coll.delete_one({"_id": ObjectId(id)})
            return "The delete was successful"
        except:
            return "The delete was failed"