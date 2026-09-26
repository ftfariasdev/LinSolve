from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, linear_system

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(linear_system.router)
