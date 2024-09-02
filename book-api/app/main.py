from fastapi import FastAPI
from app.delivery.httpsvc.routes import router as http_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the allowed origins like ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],  # Or specify the allowed methods like ["GET", "POST"]
    allow_headers=["*"],  # Or specify the allowed headers like ["Authorization"]
)


app.include_router(http_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
