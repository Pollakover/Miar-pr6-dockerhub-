from typing import List
from uuid import UUID
from app.models.notification import Notification

notifications: List[Notification] = []

class NotificationRepo:
    def list_notifications(self) -> List[Notification]:
        return notifications

    def create_notification(self, notification: Notification) -> Notification:
        notifications.append(notification)
        return notification

    def get_notification(self, id: UUID) -> Notification:
        for n in notifications:
            if n.id == id:
                return n
        raise KeyError("Notification not found")
