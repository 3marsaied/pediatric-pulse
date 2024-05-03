from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import session
from typing import List

import sys

sys.path.append('BackEnd')

import models
import DataBase
import oauth2
import utils
import schemas

router = APIRouter(
    tags=["reviews"]
)

@router.post("/add/review", status_code=status.HTTP_201_CREATED, description="This is a post request add a new review")
async def add_review(review: schemas.reviews, token:str, db: session = Depends(DataBase.get_db)):
    token_data = oauth2.verify_access_token(review.parentId, token)
    if not token_data:
        return {"message": "unauthorized"}
    if token_data == False:
        return {"message": "unauthorized"}
    
    newReview = models.reviews(parentId=review.parentId, doctorId=review.doctorId, review=review.review, rating = review.rating)
    db.add(newReview)
    db.commit()
    db.refresh(newReview)
    return {'message': "your review has been added successfully"}


@router.get("/get/review/{doctorId}", status_code=status.HTTP_200_OK, description="This is a get request to get all reviews of a patient", response_model=List[schemas.reviewsResponse])
async def get_review(doctorId: int, db: session = Depends(DataBase.get_db)):
    reviews = db.query(models.reviews).filter(models.reviews.doctorId ==doctorId).all()
    reviews_response = []
    for review in reviews:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == review.doctorId).first()
        reviewer = db.query(models.User).filter(models.User.userId == review.parentId).first()
        doctorName = "Dr. " + doctor.firstName + " " + doctor.lastName
        reviewerName = reviewer.firstName + " " + reviewer.lastName
        reviews_response.append(schemas.reviewsResponse(
            reviewerName = reviewerName,
            docotrName = doctorName,
            review = review.review,
            rating = review.rating
        ))
    return reviews_response