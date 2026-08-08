from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import (get_db,get_current_user)
from app.schemas.notification import (NotificationResponse)
from app.repository import notification_repository

router = APIRouter(prefix="/notifications",
                    tags=["Notifications"])

@router.get("",response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    return notification_repository.get_notifications(db,current_user.id)

@router.get("/unread",response_model=list[NotificationResponse])
def unread_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    return notification_repository.get_unread_notifications(db,current_user.id)

@router.put("/{notification_id}/read",response_model=NotificationResponse)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    notification = notification_repository.get_notification_by_id(db,notification_id)
    if not notification:
        raise HTTPException(status_code=404,
                            detail="Notification not found.")
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    return notification_repository.mark_as_read(db,notification)

@router.put("/read-all")
def mark_all(db: Session = Depends(get_db),
            current_user=Depends(get_current_user)):
    notification_repository.mark_all_read(db,current_user.id)
    return {"message": "All notifications marked as read."}

@router.get("",response_model=list[NotificationResponse])
def notifications(
    page: int = 1,
    size: int = 10,
    unread: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):
    return notification_repository.get_notifications(db,current_user.id,page,size,unread)