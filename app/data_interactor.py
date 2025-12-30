class Contact:
    def __init__(self, first_name:str, last_name:str, phone_number:str, id:int|None = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def to_dict(self):
        return self.__dict__
    
