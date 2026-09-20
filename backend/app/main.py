from fastapi import FastAPI

from app.routes.services import router as services_router
from app.routes.incidents import router as incidents_router
from app.routes.users import router as users_router
from app.routes.logs import router as logs_router
from app.routes.comments import router as comments_router

app = FastAPI(
    title="OpsMind AI",
    description="AI-powered IT Incident Management Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "OpsMind AI API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(services_router)
app.include_router(incidents_router)
app.include_router(users_router)
app.include_router(logs_router)
app.include_router(comments_router)
