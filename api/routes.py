from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from lead_generation.core import generate_leads
from lead_generation.schemas import LeadGenerationRequest, LeadGenerationResponse
import traceback
import os

def create_app() -> FastAPI:
    app = FastAPI(title="Lead Generation API")

    # CORS configuration - allow Vercel and local development
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Add production Vercel URLs from environment
    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        allowed_origins.append(f"https://{vercel_url}")
    
    # Add custom frontend URL from environment
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        allowed_origins.append(frontend_url)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with allowed_origins for security
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {"status": "ok", "message": "LeadFinder API is running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.post("/generate-leads", response_model=LeadGenerationResponse)
    async def create_lead_generation(request: LeadGenerationRequest):
        try:
            result = generate_leads(request.query, request.num_links)
            
            if not result:
                # Return empty results instead of 404
                return LeadGenerationResponse(urls=[], user_data=[])
            
            return LeadGenerationResponse(**result)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    return app