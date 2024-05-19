from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import session
from typing import List
import pprint

import sys

sys.path.append('BackEnd')

import models
import DataBase
import oauth2
import utils
import schemas

router = APIRouter(
    tags=["Appointment"]
)


@router.post("/add/appointment", status_code=status.HTTP_201_CREATED, description="This is a post request add a new appointment")
async def add_appointment(appointment: schemas.addApointment, token: str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(appointment.parentId, token)
    if not token_data:
        raise HTTPException( status_code=401, detail= "unauthorized")
    if token_data == False:
        raise HTTPException( status_code=401, detail= "unauthorized")

    Appointment = db.query(models.Appointment).filter(models.Appointment.appointmentDate == appointment.appointmentDate).filter(models.Appointment.From == appointment.From).filter(models.Appointment.To == appointment.To).first()
    if Appointment:
        return {"message": " Appointment already exists"}
    new_appointment = models.Appointment(
        parentId = appointment.parentId,
        doctorId = appointment.doctorId,
        patientId = appointment.patientId,
        appointmentDate = appointment.appointmentDate,
        From = appointment.From,
        To = appointment.To,
        isTaken = appointment.isTaken
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    if not db.query(models.MRAccess).filter(models.MRAccess.patientId == appointment.patientId).filter(models.MRAccess.doctorId == appointment.doctorId).first():
        mra = models.MRAccess(
            patientId = appointment.patientId,
            doctorId = appointment.doctorId
        )
        db.add(mra)
        db.commit()
        db.refresh(mra)
    
    return{"message": "Appointment added successfully"}

@router.get("/get/appointment/{parentId}", status_code=status.HTTP_200_OK, description="This is a get request to get all appointments of a patient")
async def get_appointment(parentId: int, token: str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(parentId, token)
    if not token_data:
        raise HTTPException( status_code=401, detail= "unauthorized")
    if token_data == False:
        raise HTTPException( status_code=401, detail= "unauthorized")
    appointments = db.query(models.Appointment).filter(models.Appointment.parentId == parentId).all()
    Data = []
    for apointment in appointments:
        user = db.query(models.User).filter(models.User.userId == apointment.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == apointment.patientId).first()
        Data.append({
            "id": apointment.id,
            "parentId": user.userId,
            "patientId": patient.id,
            "doctorId": apointment.doctorId,
            "patientFirstName": patient.firstName,
            "parentFirstName": user.firstName,
            "parentLastName": user.lastName,
            "parentPic": user.profilePicture,
            "appointmentDate": apointment.appointmentDate,
            "From": apointment.From,
            "To": apointment.To,
            "isTaken": apointment.isTaken,
        })
    return Data


@router.get("/get/doctor/appointments/table/{doctorId}/{userId}", status_code=status.HTTP_200_OK, description="This is a get request to get all appointments of a patient")
async def get_appointment(doctorId: int, userId: int, token: str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(userId, token)
    if not token_data:
        raise HTTPException( status_code=401, detail= "unauthorized")
    appointments = db.query(models.Appointment).filter(models.Appointment.doctorId == doctorId).all()
    Data = []
    for apointment in appointments:
        user = db.query(models.User).filter(models.User.userId == apointment.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == apointment.patientId).first()
        Data.append({
            "appointmentId": apointment.id,
            "parentId": user.userId,
            "patientId": patient.id,
            "patientFirstName": patient.firstName,
            "parentFirstName": user.firstName,
            "parentLastName": user.lastName,
            "parentPic": user.profilePicture,
            "appointmentDate": apointment.appointmentDate,
            "From": apointment.From,
            "To": apointment.To,
            "isTaken": apointment.isTaken,
        })
    return Data



@router.get('/get/all/appointments', description="This route returns all appointments")
async def get_appointment(adminId: int, token: str, db: session = Depends(DataBase.get_db)):
    
    appointments = db.query(models.Appointment).all()
    Data = []
    
    for appointment in appointments:
        user = db.query(models.User).filter(models.User.userId == appointment.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == appointment.patientId).first()
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()
        
        appointment_data = {
            "appointmentId": appointment.id,
            "parentId": user.userId,
            "patientId": patient.id,
            "doctorId": doctor.id,
            "patientFirstName": patient.firstName,
            "parentFirstName": user.firstName,
            "parentLastName": user.lastName,
            "doctorFirstName": doctor.firstName,
            "doctorLastName": doctor.lastName,
            "parentPic": user.profilePicture,
            "appointmentDate": appointment.appointmentDate,
            "From": appointment.From,
            "To": appointment.To,
            "isTaken": appointment.isTaken,
        }
        
        Data.append(appointment_data)
    
    return Data 


@router.get("/get/all/appointments/table/{adminId}", status_code=status.HTTP_200_OK, description="This is a get request to get all appointments of a patient")
async def get_appointment(adminId: int, token: str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(adminId, token)
    if not token_data:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    appointments = db.query(models.Appointment).all()
    Data = []
    
    for appointment in appointments:
        user = db.query(models.User).filter(models.User.userId == appointment.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == appointment.patientId).first()
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()
        
        appointment_data = {
            "appointmentId": appointment.id,
            "parentId": user.userId,
            "patientId": patient.id,
            "doctorId": doctor.id,
            "patientFirstName": patient.firstName,
            "parentFirstName": user.firstName,
            "parentLastName": user.lastName,
            "doctorFirstName": doctor.firstName,
            "doctorLastName": doctor.lastName,
            "parentPic": user.profilePicture,
            "appointmentDate": appointment.appointmentDate,
            "From": appointment.From,
            "To": appointment.To,
            "isTaken": appointment.isTaken,
        }
        
        Data.append(appointment_data)
    
    return Data 


@router.get('/get/all/appointments/{staffId}', description="This route returns all appointments")
async def get_all_appointments(staffId: int, token: str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(staffId, token)
    if not token_data:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    appointments = db.query(models.Appointment).all()
    Data = []
    
    for appointment in appointments:
        user = db.query(models.User).filter(models.User.userId == appointment.parentId).first()
        patient = db.query(models.Patient).filter(models.Patient.id == appointment.patientId).first()
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctorId).first()
        
        appointment_data = {
            "appointmentId": appointment.id,
            "parentId": user.userId,
            "patientId": patient.id,
            "doctorId": doctor.id,
            "patientFirstName": patient.firstName,
            "parentFirstName": user.firstName,
            "parentLastName": user.lastName,
            "doctorFirstName": doctor.firstName,
            "doctorLastName": doctor.lastName,
            "parentPic": user.profilePicture,
            "appointmentDate": appointment.appointmentDate,
            "From": appointment.From,
            "To": appointment.To,
            "isTaken": appointment.isTaken,
        }
        
        Data.append(appointment_data)
    
    # Print the response structure for inspection
    pprint.pprint(Data)

    return Data



@router.put('/update/appointments/{adminId}/{appointmentId}', description="This route updates the appointment's info")
async def update_appointments(
    adminId: int,
    appointmentId: int,
    token: str,
    appointment: schemas.updateAppointment,
    db: session = Depends(DataBase.get_db)
):
    token_data = oauth2.verify_access_token(adminId, token)
    if not token_data:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    appointment_query = db.query(models.Appointment).filter(models.Appointment.id == appointmentId)
    existing_appointment = appointment_query.first()
    
    if not existing_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = {
        "appointmentDate": appointment.appointmentDate if appointment.appointmentDate is not None else existing_appointment.appointmentDate,
        "From": appointment.From if appointment.From is not None else existing_appointment.From,
        "To": appointment.To if appointment.To is not None else existing_appointment.To,
        "isTaken": appointment.isTaken if appointment.isTaken is not None else existing_appointment.isTaken
    }

    appointment_query.update(update_data)
    db.commit()

    new_appointment = appointment_query.first()

    return new_appointment


@router.delete("/delete/appointment/{appointmentId}/{adminId}", status_code=status.HTTP_200_OK, description="This is a delete request to delete an appointment")
async def delete_appointment(appointmentId: int, adminId:int, token: str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(adminId, token)
    if not token_data:
        raise HTTPException( status_code=401, detail= "unauthorized")
    if token_data == False:
        raise HTTPException( status_code=401, detail= "unauthorized")
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointmentId).first()
    mra = db.query(models.MRAccess).filter(models.MRAccess.patientId == appointment.patientId).filter(models.MRAccess.doctorId == appointment.doctorId).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    db.delete(appointment)
    db.commit()
    appointment = db.query(models.Appointment).filter(models.Appointment.patientId == appointment.patientId).filter(models.Appointment.doctorId == appointment.doctorId).first()
    if not appointment:
        db.delete(mra)
        db.commit()
    return {"message": "Patient deleted successfully"}
