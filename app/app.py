from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from .schemas import PostCreate, PostResponse
from .db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifesepan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifesepan)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    post = Post(
        caption=caption, url="dummy url", file_type="photo", file_name="dummy name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return {
        "id": post.id,
        "caption": post.caption,
        "url": post.url,
        "file name": post.file_name,
        "file type": post.file_type,
    }
