# app/main.py
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.helpers.auth import verify_bearer_token  # Import the token verification function
from .config.database import Base, engine
from .api import application_router  # Import application routes
from dotenv import load_dotenv
import uvicorn
import argparse

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Exposes all headers in the response
)

app.include_router(application_router, dependencies=[Depends(verify_bearer_token)])


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint to check the health of the API.
    Requires a valid JWT token for access.
    """
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    config = uvicorn.Config("app.main:app", port=args.port, log_level="info", reload=True)
    server = uvicorn.Server(config)
    print(f"Server is running at http://127.0.0.1:{config.port}")
    server.run()