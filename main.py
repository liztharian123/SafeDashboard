import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.database import async_engine, get_db
from app.middleware.logging_middleware import LoggingMiddleware
from app.routers import dashboard_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()


app = FastAPI(title="SafeDashboard", lifespan=lifespan)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(dashboard_router.router)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if "text/html" in request.headers.get("accept", ""):
        return HTMLResponse(
            content="<h2>404 – Page not found</h2><p><a href='/dashboard'>Go to Dashboard</a></p>",
            status_code=404,
        )
    return JSONResponse(status_code=404, content={"detail": "Not found"})


@app.get("/health")
async def health_check():
    async for session in get_db():
        await session.execute(text("SELECT 1"))
    return JSONResponse({"status": "ok"})


@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
