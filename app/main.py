from app.api.v1.api import router as api_router
from app.config import settings
from starlette.middleware import Middleware
from app.middleware import LoggingMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import secrets
from app.models.dbinit import init_db



init_db()# Initialize the database



origins = [
    "https://login.microsoftonline.com",
    "*"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=["Content-Type", "Authorization", "Set-Cookie", "Access-Control-Allow-Origin"],
    ),
    Middleware(
        SessionMiddleware,
        secret_key=secrets.token_urlsafe(32),
    ),

]


app = FastAPI(
    title="Integrador SMAX",
    docs_url="/docs",
    openapi_url="/openapi.json",
    middleware=middleware,
    root_path=settings.root_path,
)

app.add_middleware(LoggingMiddleware)
# app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))


@app.get("/health")
async def health():
    return {"message": "STATUS: ok"}

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

app.include_router(api_router, prefix="/api")