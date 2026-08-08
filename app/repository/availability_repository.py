from sqlalchemy.orm import Session
from app.models.availability import Availability
from datetime import date, time

def create_availability(db: Session, availability: Availability):
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability

def get_availability_by_id(db: Session, availability_id: int):
    return (db.query(Availability)
            .filter(Availability.id == availability_id)
            .first())

def get_provider_slots(db: Session, provider_id: int):
    return (db.query(Availability)
            .filter(Availability.provider_id == provider_id)
            .all())

def check_overlap(db: Session,provider_id: int,slot_date: date,start_time: time,end_time: time):
    return (db.query(Availability).filter(
            Availability.provider_id == provider_id,
            Availability.date == slot_date,
            Availability.start_time < end_time,
            Availability.end_time > start_time).first())

def update_availability(db: Session, availability: Availability):
    db.commit()
    db.refresh(availability)
    return availability


def delete_availability(db: Session, availability: Availability):
    db.delete(availability)
    db.commit()