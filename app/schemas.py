from pydantic import BaseModel 

class UserCreate (BaseModel): 
    email: str 
    password :str 
class UserRead (BaseModel) : 
    int : id
    email : str

