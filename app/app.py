from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from .schemas import PostCreate, PostResponse, UserRead, UserCreate, UserUpdate
from .db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from .images import imageKit
import shutil
import os
import uuid
import tempfile
import logging
from .users import auth_backend, current_active_user, fastapi_users

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifesepan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifesepan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/auth",
    tags=["auth"],
)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
):
    temp_file_path = None
    temp_file_obj = None

    try:
        # Validate ImageKit credentials
        if not imageKit.private_key:
            raise ValueError("IMAGEKIT_PRIVATE_KEY environment variable is not set")

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # Read file into bytes
        temp_file_obj = open(temp_file_path, "rb")
        file_data = temp_file_obj.read()
        temp_file_obj.close()

        logger.info(f"Uploading file: {file.filename}")
        upload_result = imageKit.files.upload(
            file=file_data,
            file_name=file.filename,
            use_unique_file_name=True,
            tags=["backend-upload"],
        )

        logger.info(f"Upload result type: {type(upload_result)}")
        logger.info(f"Upload result: {upload_result}")
        logger.info(f"Upload result attributes: {dir(upload_result)}")

        if upload_result.file_id:

            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type=(
                    "video" if file.content_type.startswith("video/") else "image"
                ),
                file_name=upload_result.file_path,
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
        else:
            error_msg = f"ImageKit upload failed: no file_id returned"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.exception(f"Error in upload_file: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")
    finally:
        if temp_file_obj:
            temp_file_obj.close()
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )
    return {"posts": post_data}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="❌ Post not found!")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "✅ Post deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error deleting post: {str(e)}")
