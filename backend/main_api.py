import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *
from database import get_db, integrity_error_detail
from routers import user as user_router
from routers import user_methods as user_methods_router
from routers import subgoal as subgoal_router
from routers import subgoal_methods as subgoal_methods_router
from routers import resolution as resolution_router
from routers import resolution_methods as resolution_methods_router
from routers import progressentry as progressentry_router
from routers import progressentry_methods as progressentry_methods_router
from routers import habit as habit_router
from routers import habit_methods as habit_methods_router
from routers import category as category_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='Class_Diagram API',
    description='Auto-generated REST API with full CRUD operations, relationship management, and advanced features',
    version='1.0.0',
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "User", "description": "Operations for User entities"},
        {"name": "User Relationships", "description": "Manage User relationships"},
        {"name": "User Methods", "description": "Execute User methods"},
        {"name": "SubGoal", "description": "Operations for SubGoal entities"},
        {"name": "SubGoal Relationships", "description": "Manage SubGoal relationships"},
        {"name": "SubGoal Methods", "description": "Execute SubGoal methods"},
        {"name": "Resolution", "description": "Operations for Resolution entities"},
        {"name": "Resolution Relationships", "description": "Manage Resolution relationships"},
        {"name": "Resolution Methods", "description": "Execute Resolution methods"},
        {"name": "ProgressEntry", "description": "Operations for ProgressEntry entities"},
        {"name": "ProgressEntry Relationships", "description": "Manage ProgressEntry relationships"},
        {"name": "ProgressEntry Methods", "description": "Execute ProgressEntry methods"},
        {"name": "Habit", "description": "Operations for Habit entities"},
        {"name": "Habit Relationships", "description": "Manage Habit relationships"},
        {"name": "Habit Methods", "description": "Execute Habit methods"},
        {"name": "Category", "description": "Operations for Category entities"},
        {"name": "Category Relationships", "description": "Manage Category relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    # The client sees a 400; the server log keeps the traceback of the real cause.
    logger.exception("ValueError on %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": integrity_error_detail(exc)
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.exception(f"Database error: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format.

    `detail` carries the endpoint's actual message — clients (including the
    generated frontend dialog) read it to show the user what went wrong.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": exc.detail
        }
    )

############################################
#
#   Routers
#
############################################

app.include_router(user_router.router)
app.include_router(user_methods_router.router)
app.include_router(subgoal_router.router)
app.include_router(subgoal_methods_router.router)
app.include_router(resolution_router.router)
app.include_router(resolution_methods_router.router)
app.include_router(progressentry_router.router)
app.include_router(progressentry_methods_router.router)
app.include_router(habit_router.router)
app.include_router(habit_methods_router.router)
app.include_router(category_router.router)

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": app.title,
        "version": app.version,
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check(database: Session = Depends(get_db)):
    """Health check endpoint for monitoring.

    Actually touches the database — a health check that hardcodes
    "connected" is worse than none.
    """
    from datetime import datetime
    from sqlalchemy import text as _sql_text
    try:
        database.execute(_sql_text("SELECT 1"))
        db_status = "connected"
    except Exception:
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "database": "error",
        })
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["user_count"] = database.query(User).count()
    stats["subgoal_count"] = database.query(SubGoal).count()
    stats["resolution_count"] = database.query(Resolution).count()
    stats["progressentry_count"] = database.query(ProgressEntry).count()
    stats["habit_count"] = database.query(Habit).count()
    stats["category_count"] = database.query(Category).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)