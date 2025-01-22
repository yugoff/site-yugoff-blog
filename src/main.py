from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging

from src.endpoints import index, stream, skills, portfolio
from src.services.database import connect_db, close_db, create_tables

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Connect to DB...')
    conn = await connect_db()
    app.state.db = conn
    try:
        logger.info('Creating tables...') 
        await create_tables(conn)
        yield
    finally:
        logger.info('Closing DB connection...')
        await close_db(conn)

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='src/static'), name='static')
app.include_router(index.router)
app.include_router(stream.router, prefix='/projects')
app.include_router(skills.router, prefix='/api')
app.include_router(portfolio.router, prefix='/api')


