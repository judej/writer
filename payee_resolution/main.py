from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Payee Resolution Service")

app.include_router(router)
