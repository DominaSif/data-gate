import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.routers import documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(settings.database_url)
    yield
    await app.state.pool.close()

app = FastAPI(title="api-shield", lifespan=lifespan)
app.include_router(documents.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
