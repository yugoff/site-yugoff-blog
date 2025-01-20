from fastapi import APIRouter, HTTPException, Request

from src.schemas.portfolio import PortfolioItem

router = APIRouter()

@router.post('/portfolio')
async def add_portfolio(request: Request, portfolio: PortfolioItem):
    conn = request.app.state.db
    try:
        query = '''
        INSERT INTO portfolio (title, image, alt, href, types)
        VALUES ($1, $2, $3, $4, $5);
        '''
        await conn.execute(query, portfolio.title, portfolio.image, portfolio.alt, portfolio.href, portfolio.types)
        return {'message': 'Portfolio added successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
