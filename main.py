from fastapi import FastAPI
import uvicorn
import logging

import acs_handler
import ai_connector
import irctc_mock

# Setup structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="Conversational IVR Modernization Framework - Integration Layer",
    description="Python FastAPI middleware connecting legacy VXML IVR, Azure Communication Services, BAP AI, and IRCTC Backend APIs",
    version="1.0.0"
)

# Include modules
app.include_router(acs_handler.router)
app.include_router(ai_connector.router)
app.include_router(irctc_mock.router)

@app.get("/health", tags=["System"])
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "IVR Integration Layer"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
