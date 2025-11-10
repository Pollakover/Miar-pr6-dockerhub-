from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment_schema import PaymentDB
from uuid import UUID

class PaymentRepo:
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_payments(self) -> list[Payment]:
        records = self.db.query(PaymentDB).all()
        return [
            Payment(
                id=UUID(r.id),
                amount=r.amount,
                currency=r.currency,
                status=r.status,
                created_at=r.created_at
            ) for r in records
        ]

    def get_payment_by_id(self, id: UUID) -> Payment:
        record = self.db.query(PaymentDB).filter(PaymentDB.id == str(id)).first()
        if not record:
            raise KeyError("Payment not found")
        return Payment(
            id=UUID(record.id),
            amount=record.amount,
            currency=record.currency,
            status=record.status,
            created_at=record.created_at
        )

    def create_payment(self, payment: Payment) -> Payment:
        db_payment = PaymentDB(
            id=str(payment.id),
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status,
            created_at=payment.created_at
        )
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return payment

    def update_status(self, payment: Payment) -> Payment:
        record = self.db.query(PaymentDB).filter(PaymentDB.id == str(payment.id)).first()
        if not record:
            raise KeyError("Payment not found")
        record.status = payment.status
        self.db.commit()
        return payment
