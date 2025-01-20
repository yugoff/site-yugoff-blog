from fastapi import APIRouter, HTTPException, Request

from src.schemas.skills import SkillsItem

router = APIRouter()

@router.post('/skills')
async def add_skills(request: Request, skills: SkillsItem):
    conn = request.app.state.db
    try:
        query = 'INSERT INTO skills (name) VALUES ($1);'
        await conn.execute(query, skills.name)
        return {'message': 'Skill added successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
