from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory='src/templates')

@router.get('/stream', response_class=HTMLResponse, summary='Получить страницу с камерами')
async def stream(request: Request):
    return templates.TemplateResponse('stream.html', {'request': request})

@router.get('/stream/api/search_stream', summary='Поиск открытых видеопотоков')
async def search_stream():
    avialable_streams = [
        {"id": 1, "url": "http://example.com/stream1", "name": "Camera 1"},
        {"id": 2, "url": "http://example.com/stream2", "name": "Camera 2"},
        {"id": 3, "url": "http://example.com/stream3", "name": "Camera 3"},
    ]
    return {'streams': avialable_streams}