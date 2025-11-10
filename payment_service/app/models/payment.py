from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class PaymentStatus(str, Enum):
    CREATED = "created"
    SUCCESS = "success"
    FAILED = "failed"
    REFUND_REQUESTED = "refund_requested"
    REFUND_DONE = "refund_done"
    REFUND_DENIED = "refund_denied"

class Payment(BaseModel):
    id: UUID
    amount: float
    currency: str = "USD"
    status: PaymentStatus = PaymentStatus.CREATED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    invoice_id: UUID | None = None
