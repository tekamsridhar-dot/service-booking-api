from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.utils.pagination import paginate

def create_notification(db: Session, notification: Notification):
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notifications(db: Session, user_id: int):
    return (db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc()).all())

def get_unread_notifications(db: Session,user_id: int):
    return (db.query(Notification)
        .filter(Notification.user_id == user_id,
                Notification.is_read == False)
        .order_by(Notification.created_at.desc()).all())

def get_notification_by_id(db: Session,notification_id: int):
    return (db.query(Notification)
            .filter(Notification.id == notification_id)
            .first())

def mark_as_read(db: Session, notification: Notification):
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification

def mark_all_read(db: Session,user_id: int):
    notifications = (db.query(Notification)
                    .filter(Notification.user_id == user_id).all())
    for notification in notifications:
        notification.is_read = True
    db.commit()
    return notifications

def get_notifications(db,user_id,page=1,size=10,unread=False):
    query = db.query(Notification)
    query = query.filter(Notification.user_id == user_id)
    if unread:
        query = query.filter(Notification.is_read == False)
        query = query.order_by(Notification.created_at.desc())
    return paginate(query,page,size)