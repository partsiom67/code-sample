from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.core.exception_handlers import app


def include_router(app):
    app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sub API",
        version="1.0.0",
        description="Sub API documentation",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def start_app(app):
    include_router(app)
    app.openapi = custom_openapi
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


start_app(app)
