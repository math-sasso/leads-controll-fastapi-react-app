from typing import List, Union
import datetime as dt
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    

class UserCreate(UserBase):
    hashed_password :str
    
    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    class Config:
        orm_mode = True


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str


class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    """T
    his class is a subclass of LeadBase. It contains the following properties:

    id: The unique identifier for the lead
    owner_id: The unique identifier for the lead owner
    date_created: The date when the lead was created
    date_last_updated: The date when the lead was last updated
    The class also contains a configuration parameter 
    orm_mode
    which is set to 
    True
    .
    This parameter indicates that the Lead class is using an Object Relational Mapping (ORM) configuration.
    """
    id: int
    owner_id:int
    date_created: dt.datetime
    date_last_updated: dt.datetime

    class Config:
        orm_mode = True

