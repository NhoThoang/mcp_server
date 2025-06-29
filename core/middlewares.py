from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mcp_Server.core.config import config_env_manager as config_app

def setup_middlewares(app: FastAPI):
    # Nếu cors_origins là "*" thì fallback theo môi trường
    if config_app.CORS_ORIGINS == ["*"]:
        if config_app.ENVIRONMENT == "production":
            allowed_origins = ["https://yourdomain.com"]
        else:
            allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"]
    else:
        print("CORS origins from config:", config_app.CORS_ORIGINS)
        allowed_origins = config_app.CORS_ORIGINS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
