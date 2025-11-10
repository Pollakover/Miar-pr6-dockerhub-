from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.dialects.sqlite import BLOB
from datetime import datetime
from uuid import uuid4
from app.database import Base
from app.models.payment import PaymentStatus

class PaymentDB(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
