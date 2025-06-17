from fastapi import FastApi
from pydantic import BaseModel


class UserInput(BaseModel):
    location:str
    bhk:int
    bathrooms:int
    sqft:int
    
    