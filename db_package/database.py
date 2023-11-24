#  @bekbrace
#  FARMSTACK Tutorial - Sunday 13.06.2021
from fastapi import  HTTPException

import motor.motor_asyncio
from models import Patient,HealthcareProfessional,Caregiver,User

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://healthcare-mongo:27017/')
database = client.healthcare_db
collection_Patient = database.Patient
collection_HealthcareProfessional = database.HealthcareProfessional
collection_Caregiver=database.Caregiver




async def fetch_all_users():
    users = []
    cursor = collection_Patient.find({})
    async for document in cursor:
        users.append(Patient(**document))
    return users

async def create_user(user):
    document = user

    if user.status == "patient":
        result = await collection_Patient.insert_one(user.dict())
    elif user.status == "healthcare_professional":
        result = await collection_HealthcareProfessional.insert_one(user.dict())
    elif user.status == "caregiver":
        result = await collection_Caregiver.insert_one(user.dict())
    else:
        raise HTTPException(400, "Wrong data entry")

    return document


async def verify_user(username, password,status):
    if status=='patient':
        user = await collection_Patient.find_one({"name": username, "password": password})
    elif  status=='healthcare_professionnal':
        user = await collection_HealthcareProfessional.find_one({"name": username, "password": password})
    elif status=='caregiver':
        user = await collection_Caregiver.find_one({"name": username, "password": password})
    else:
        HTTPException(400, "Something went wrong")


    return user

async def get_user_by_name(name,status):
    if status=='patient':
        user = await collection_Patient.find_one({"name": name})
    elif  status=='healthcare_professionnal':
        user = await collection_HealthcareProfessional.find_one({"name": name})
    elif status=='caregiver':
        user = await collection_Caregiver.find_one({"name": name})
    else:
        user =None
    return user


async def count_patients_above_memory_score(cutoff: int) -> int:
    count = await collection_Patient.count_documents({
        "$and": [
            {"status": "patient"},
            {"memory_score": {"$gt": cutoff}}
        ]
    })
    return count

async def count_patients_above_memory_and_age( memory_cutoff: int, age_cutoff: int) -> int:
    count = await collection_Patient.count_documents({
        "$and": [
            {"status": "patient"},
            {"memory_score": {"$gt": memory_cutoff}},
            {"age": {"$ne": age_cutoff}}
        ]
    })
    return count

async def init():
    await collection_Patient.insert_one({"name": "Patient1", "password": "pass1", "status": "patient", "age": 25, "memory_score": 90})
    await collection_HealthcareProfessional.insert_one({"name": "HealthcareProfessional1", "password": "pass2", "status": "healthcare_professional", "type": "neurologist"})
    await collection_Caregiver.insert_one({"name": "Caregiver1", "password": "pass3", "status": "caregiver", "related_patient": None})