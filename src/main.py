"""
Main FastAPI Application

This is the main entry point for the Unifly Backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import APP_NAME, APP_VERSION, CORS_ORIGINS
from src.api import api_router

# Create the FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Unifly Backend API for university application management",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Unifly Backend API",
        "version": APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "unifly-backend"}

if __name__ == "__main__":
    import uvicorn
    from src.config import API_HOST, API_PORT
    
    uvicorn.run(
        "src.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )

