from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class NotificationType(str, Enum):
    BOOKING_CONFIRMED = "booking_confirmed"
    BOOKING_CANCELED = "booking_canceled"
    ORDER_PLACED = "order_placed"
    CLEANING_DONE = "cleaning_done"
    SHIFT_ASSIGNED = "shift_assigned"
    SHIFT_EXTENDED = "shift_extended"
    SHIFT_SHORTENED = "shift_shortened"
    SHIFT_REALLOCATED = "shift_reallocated"
    REVIEW_REJECTED = "review_rejected"

class NotificationStatus(str, Enum):
    SENT = "sent"
    FAILED = "failed"

class Notification(BaseModel):
    id: UUID
    type: NotificationType
    message: str
    recipient: str | None = None
    status: NotificationStatus = NotificationStatus.SENT
    created_at: datetime = Field(default_factory=datetime.utcnow)
