from fastapi import FastAPI
from app.endpoints.payment_router import router as payment_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment Service")
app.include_router(payment_router, prefix="/api/payments")
