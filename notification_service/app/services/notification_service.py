from uuid import uuid4, UUID
from datetime import datetime
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.repositories.local_notification_repo import NotificationRepo

class NotificationService:
    def __init__(self):
        self.repo = NotificationRepo()

    def send(self, n_type: NotificationType, message: str, recipient: str | None = None) -> Notification:
        notif = Notification(id=uuid4(), type=n_type, message=message, recipient=recipient, status=NotificationStatus.SENT, created_at=datetime.utcnow())
        return self.repo.create_notification(notif)

    def list(self):
        return self.repo.list_notifications()

    def get(self, id: UUID):
        return self.repo.get_notification(id)
