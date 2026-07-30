from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models

from app.routers import (
    auth,
    users,
    farms,
    investments,
    reports,
    marketplace,
    ai_assistant,
    settings,
    dashboard,
)


# =====================================================
# Application Lifespan
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Debug: show registered tables
    print("Registered tables:")
    print(list(Base.metadata.tables.keys()))

    # Create database tables
    Base.metadata.create_all(bind=engine)

    print("✅ AquaVest API started successfully.")

    yield

    print("🛑 AquaVest API stopped.")


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="AquaVest API",
    description="Backend API for the AquaVest Fish Farming Investment Platform.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# =====================================================
# CORS Configuration
# =====================================================

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Register Routers
# =====================================================

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(farms.router)
app.include_router(investments.router)
app.include_router(reports.router)
app.include_router(marketplace.router)
app.include_router(ai_assistant.router)
app.include_router(settings.router)
app.include_router(dashboard.router)


# =====================================================
# Root Endpoint
# =====================================================

@app.get("/", tags=["System"])
def root():
    return {
        "application": "AquaVest API",
        "description": "Fish Farming Investment Platform",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "health": "/health",
    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "service": "AquaVest API",
        "version": "1.0.0",
    }


# =====================================================
# API Version
# =====================================================

@app.get("/version", tags=["System"])
def version():
    return {
        "application": "AquaVest API",
        "version": "1.0.0",
    }