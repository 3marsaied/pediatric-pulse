from fastapi import FastAPI
from DataBase import engine
from models import base
from routes import auth, user, doctor, patient, appointment

from fastapi.middleware.cors import CORSMiddleware

base.metadata.create_all(bind=engine)

# Define other components of your application
app = FastAPI()
#app.include_router(auth.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


