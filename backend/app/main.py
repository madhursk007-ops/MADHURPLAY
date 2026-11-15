from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from .config import settings
from .database import Base, engine, get_db
from .models import User, WatchlistItem
from .schemas import RegisterIn, LoginIn, TokenOut, WatchlistIn, WatchlistOut
from .security import hash_password, verify_password, create_token, current_user, admin_user
from .tmdb import tmdb

Base.metadata.create_all(bind=engine)
app = FastAPI(title="MADHURPLAY API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"name": "MADHURPLAY API", "status": "online"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/register", response_model=TokenOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(400, "Password must contain at least 8 characters")
    if db.scalar(select(User).where(User.email == data.email.lower())):
        raise HTTPException(409, "Email is already registered")
    user = User(email=data.email.lower(), password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user)}

@app.post("/api/auth/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_token(user)}

@app.get("/api/movies/trending")
async def trending():
    return await tmdb("trending/movie/week")

@app.get("/api/movies/search")
async def search_movies(q: str, page: int = 1):
    return await tmdb("search/movie", {"query": q, "page": page, "include_adult": "false"})

@app.get("/api/movies/genres")
async def genres():
    return await tmdb("genre/movie/list")

@app.get("/api/movies/{movie_id}")
async def movie_detail(movie_id: int):
    return await tmdb(f"movie/{movie_id}", {"append_to_response": "videos,credits"})

@app.get("/api/watchlist", response_model=list[WatchlistOut])
def get_watchlist(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.scalars(select(WatchlistItem).where(WatchlistItem.user_id == user.id)).all()

@app.post("/api/watchlist", response_model=WatchlistOut)
def add_watchlist(data: WatchlistIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(WatchlistItem).where(WatchlistItem.user_id == user.id, WatchlistItem.movie_id == data.movie_id))
    if item:
        return item
    item = WatchlistItem(user_id=user.id, **data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@app.delete("/api/watchlist/{movie_id}")
def remove_watchlist(movie_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(WatchlistItem).where(WatchlistItem.user_id == user.id, WatchlistItem.movie_id == movie_id))
    if not item:
        raise HTTPException(404, "Movie not found in watchlist")
    db.delete(item); db.commit()
    return {"removed": True}

@app.get("/api/admin/overview")
def admin_overview(_: User = Depends(admin_user), db: Session = Depends(get_db)):
    return {"users": db.query(User).count(), "watchlist_entries": db.query(WatchlistItem).count()}
