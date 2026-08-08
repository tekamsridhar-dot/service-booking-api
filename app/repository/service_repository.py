from sqlalchemy.orm import Session
from app.models.service import Service
from app.utils.pagination import paginate

def create_service(db: Session, service: Service):
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def get_service_by_id(db: Session, service_id: int):
    return (
        db.query(Service)
        .filter(Service.id == service_id)
        .first())

def get_services(
    db,
    page=1,
    size=10,
    search=None,
    category=None,
    min_price=None,
    max_price=None,
    sort_by=None):

    query = db.query(Service)
    query = query.filter(
        Service.status == "Active")
    if search:
        query = query.filter(Service.service_name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Service.category == category)
    if min_price is not None:
        query = query.filter(Service.price >= min_price)
    if max_price is not None:
        query = query.filter(Service.price <= max_price)
    if sort_by == "price":
        query = query.order_by(Service.price)
    elif sort_by == "-price":
        query = query.order_by(Service.price.desc())
    elif sort_by == "name":
        query = query.order_by(Service.service_name)
    return paginate(query,page,size)

def update_service(db: Session, service: Service):
    db.commit()
    db.refresh(service)
    return service

def delete_service(db: Session, service: Service):
    service.is_deleted = True
    db.commit()
    db.refresh(service)
    return service



