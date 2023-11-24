
from fastapi import FastAPI, HTTPException,Depends,status

from db_package.models import Patient,HealthcareProfessional,Caregiver,loginUser
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from prometheus_fastapi_instrumentator import Instrumentator

from datetime import datetime, timedelta
from db_package.database import (
    init,
    fetch_all_users,
    get_user_by_name,
    create_user,
    verify_user,
    count_patients_above_memory_score,
    count_patients_above_memory_and_age

)



SECRET_KEY = "your-secret-key9988223344"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()
# Prometheus instrumentation
Instrumentator().instrument(app).expose(app)


# origins = [
#     "http://localhost:3000",
# ]

# what is a middleware? 
# software that acts as a bridge between an operating system or database and applications, especially on a network.


def create_jwt_token(data: dict, expires_delta: timedelta = None):
    data['sub']['_id']=str(data['sub']['_id'])

    to_encode = data['sub'].copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




# Dependency to get the current user based on the provided token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return name


@app.get("/")
async def read_root():
    return {"Hello": "first API"}


@app.get("/api/users")
async def get_todo():
    response = await fetch_all_users()
    return response



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


@app.post("/login")
async def login_for_access_token(form_data:loginUser):
    user = await verify_user(form_data.username, form_data.password,form_data.status)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(data={"sub": user}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}



    
@app.post("/create", response_model= Union[Patient, HealthcareProfessional, Caregiver])
async def create_user_api(user:Union[Patient, HealthcareProfessional, Caregiver]):
    existing_user = await get_user_by_name(user.name,user.status)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    if user.status not in ['healthcare_professionnal','patient','caregiver'] :

        raise HTTPException(status_code=400, detail="bad status")

    if user.status=='healthcare_professionnal' and  user.type not in['neurologist','general_practitionner','psychologist']:
            
        raise HTTPException(status_code=400, detail="bad type")
    
    response = await create_user(user)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")



@app.get("/api/patients/memory_score/{cutoff}", response_model=int)
async def count_patients_above_memory_score_api(cutoff: int):
    count = await count_patients_above_memory_score( cutoff)
    return count

@app.get("/api/patients/memory_age_score/{memory_cutoff}/{age_cutoff}", response_model=int)
async def count_patients_above_memory_and_age_api(
    memory_cutoff: int,
    age_cutoff: int,
):
    # Add your authentication logic here if needed (e.g., checking user roles or permissions).

    count = await count_patients_above_memory_and_age(memory_cutoff, age_cutoff)
    return count




    


async def startup_event():
    # Create base documents or perform any other initialization tasks here
    # Example: Creating base Patient, HealthcareProfessional, and Caregiver documents
    await init()

# Register the startup event
app.add_event_handler("startup", startup_event)