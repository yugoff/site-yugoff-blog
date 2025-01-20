from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src.endpoints import index, skills, portfolio
from src.services.database import connect_db, close_db, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connect to DB...")
    conn = await connect_db()
    app.state.db = conn
    try:
        print("Creating tables...") 
        await create_tables(conn)
        yield
    finally:
        print("Closing DB connection...")
        await close_db(conn)

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='src/static'), name='static')
app.include_router(index.router)
app.include_router(skills.router, prefix="/api")
app.include_router(portfolio.router, prefix="/api")


