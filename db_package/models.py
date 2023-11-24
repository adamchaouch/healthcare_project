# Pydantic allows auto creation of JSON Schemas from models
from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    name: str
    password: str
    status:str

class Patient(User):
    age: int
    memory_score: int

class HealthcareProfessional(User):
    type: str  # Assuming there are different types of healthcare professionals

class Caregiver(User):
    related_patient: Optional[Patient] = None  # Use the Patient class for the related patient

###########

class loginUser(BaseModel):
    username:str
    password:str
    status:str

