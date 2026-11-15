import httpx
from fastapi import HTTPException
from .config import settings

BASE = "https://api.themoviedb.org/3"

async def tmdb(path: str, params: dict | None = None):
    if not settings.tmdb_api_read_access_token:
        raise HTTPException(status_code=503, detail="TMDB is not configured on the backend")
    headers = {"Authorization": f"Bearer {settings.tmdb_api_read_access_token}", "accept": "application/json"}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"{BASE}/{path.lstrip('/')}", headers=headers, params=params or {})
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="Movie provider request failed")
    return response.json()
