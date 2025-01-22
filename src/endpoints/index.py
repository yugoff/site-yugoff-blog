from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request

router = APIRouter()
templates = Jinja2Templates(directory='src/templates')

@router.get('/', response_class=HTMLResponse, summary='Получить главную страницу')
async def main(request: Request):
    conn = request.app.state.db
    try:
        skills_query = 'SELECT name FROM skills;'
        skills = await conn.fetch(skills_query)
        skills_data = [
            {
            'name': skill['name']
            } 
            for skill in skills
        ]

        portfolio_query = 'SELECT title, image, alt, href, types FROM portfolio;'
        portfolio = await conn.fetch(portfolio_query)
        portfolio_data = [
            {
                'title': item['title'], 
                'image': item['image'], 
                'alt': item['alt'], 
                'href': item['href'], 
                'types': item['types']
            } 
            for item in portfolio
        ]

        return templates.TemplateResponse('index.html', {'request': request, 'skills': skills_data, 'portfolio': portfolio_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
