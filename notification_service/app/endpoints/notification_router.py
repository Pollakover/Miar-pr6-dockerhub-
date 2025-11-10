from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.notification_service import NotificationService
from app.models.notification import Notification, NotificationType
from pydantic import BaseModel

router = APIRouter()

def get_service() -> NotificationService:
    return NotificationService()

class SendRequest(BaseModel):
    type: NotificationType
    message: str
    recipient: str | None = None

@router.post("/", response_model=Notification)
def send(req: SendRequest, service: NotificationService = Depends(get_service)):
    return service.send(req.type, req.message, req.recipient)

@router.get("/", response_model=list[Notification])
def list_notifications(service: NotificationService = Depends(get_service)):
    return service.list()

@router.get("/{notification_id}", response_model=Notification)
def get_notification(notification_id: str, service: NotificationService = Depends(get_service)):
    try:
        return service.get(notification_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Notification not found")
