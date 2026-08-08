from app.models.notification import Notification
from app.repository import notification_repository

def send_notification(db,user_id,title,message):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message)
    return notification_repository.create_notification(db,notification)