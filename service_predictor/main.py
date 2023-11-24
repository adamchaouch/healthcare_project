
from fastapi import FastAPI, HTTPException,Depends
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db_package.database import (
    get_user_by_name,
 

)

# an HTTP-specific exception class  to generate exception information


SECRET_KEY = "your-secret-key9988223344"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# Prometheus instrumentation
Instrumentator().instrument(app).expose(app)





@app.get("/")
async def read_root():
    return {"Hello": "second API"}


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







# Second API: Healthcare professionals can predict the future memory_score of the patient
@app.get("/predict_patient/{username}", response_model=int)
async def predict_future_memory_score(
    username: str,
    current_user = Depends(get_current_user)
):
    # Check if the user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Check if the user is a healthcare professional (neurologist or general practitioner)
    user = await get_user_by_name(current_user['name'],current_user['status'])
    if not user or user['type'] not in ['neurologist', 'general_practitioner'] or user['status'] not in  'healthcare_professionnal':
        raise HTTPException(status_code=403, detail="Unauthorized. Only healthcare_professionnal  neurologists or general practitioners can access this API.")

    # Retrieve patient information
    patient = await get_user_by_name(username,'patient')
    # Check if the patient exists and is a patient
    if not patient or patient['status'] != 'patient':
        raise HTTPException(status_code=404, detail=f"Patient {username} not found.")

    # Predict the future memory_score based on the specified algorithm

    if patient['age'] > 50:
        return patient['memory_score'] + 5
    else:
        return patient['memory_score'] + 3
    
