from fastapi import FastAPI

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