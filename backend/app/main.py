import platform
import psutil

from app.configs.logging import setup_logging
from app.configs.errors import BadRequest, Unauthorized, Forbidden, InternalError, NotFound

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.deps.permissions_checker import PermissionChecker
from app.routes.v1.users.users_routes import router as users_routes
from app.routes.v1.auth.auth_routes import router as auth_routes
from app.routes.v1.movies.movies_routes import router as movies_routes

from app.data.mongo_connection import get_db_bevflix, connect_and_init_db, close_db

app = FastAPI(description='Bevflix Api')

setup_logging()
Instrumentator(excluded_handlers=["/app_metrics", "/health"],).instrument(app).expose(app, 
                                                                                      endpoint='/app_metrics', 
                                                                                      tags=['Metrics'],
                                                                                      include_in_schema=True)

@app.on_event("startup")
async def startup():
    await connect_and_init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.exception_handler(Forbidden)
async def forbidden_req_handler(req: Request, exc: Forbidden) -> JSONResponse:
    return exc.gen_error_response()

@app.exception_handler(Unauthorized)
async def unauthorized_req_handler(req: Request, exc: Unauthorized) -> JSONResponse:
    return exc.gen_error_response()

@app.exception_handler(BadRequest)
async def badrequest_req_handler(req: Request, exc: BadRequest) -> JSONResponse:
    return exc.gen_error_response()

@app.exception_handler(NotFound)
async def not_found_req_handler(req: Request, exc: BadRequest) -> JSONResponse:
    return exc.gen_error_response()

@app.exception_handler(InternalError)
async def internal_error_req_handler(req: Request, exc: InternalError) -> JSONResponse:
    return exc.gen_error_response()

@app.exception_handler(RequestValidationError)
async def invalid_req_handler(req: Request, exc: RequestValidationError) -> JSONResponse:
    errors: dict = {}
    for error in exc.errors():
        errors[error['loc'][1]] = error['msg']

    return JSONResponse(
        status_code=400,
        content={
            "detail": errors
        }
    )

@app.get('/', tags=['Health Check'])
@app.get('/health', tags=['Health Check'])
async def health_check(__: bool = Depends(PermissionChecker(required_permissions=['admin:health'])),
                       db_bevflix = Depends(get_db_bevflix)):
    try:
        await db_bevflix.command('ping')
        db_status = 'up'
    except Exception:
        db_status = 'down'

    system_info = {
        "system": platform.system(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage('/')._asdict()
    }

    return { 
            "db_bevflix": db_status,
            "system_info": system_info 
            }


app.include_router(auth_routes)
app.include_router(users_routes)
app.include_router(movies_routes)