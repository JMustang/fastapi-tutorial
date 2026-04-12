from fastapi import FastAPI, HTTPException
from .schemas import PostCreate, PostResponse
from .db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifesepan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifesepan)

text_posts = {
    1: {"title": "1 post", "content": "code post"},
    2: {"title": "2 post", "content": "car post"},
    3: {"title": "3 post", "content": "money post"},
    4: {"title": "4 post", "content": "music post"},
    5: {"title": "5 post", "content": "books post"},
    6: {"title": "6 post", "content": "snickers post"},
    7: {"title": "7 post", "content": "food post"},
    8: {"title": "8 post", "content": "hobby post"},
    9: {"title": "9 post", "content": "work post"},
}


@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.get("/post/{id}")
def get_posts_by_id(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="❌ Post not found!")
    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post


@app.delete("/post/{id}")
def delete_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="❌ Post not found!")
    del text_posts[id]
    return {"message": "✅ Post deleted successfully!"}
