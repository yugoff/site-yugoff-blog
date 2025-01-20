from pydantic import BaseModel

class PortfolioItem(BaseModel):
    title: str
    image: str
    alt: str
    href: str
    types: str