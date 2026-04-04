from fastapi import FastAPI, HTTPException

app = FastAPI()

text_post = {1: {"title": "1 post", "content": "code post"}}
text_post = {2: {"title": "2 post", "content": "car post"}}
text_post = {3: {"title": "3 post", "content": "money post"}}
text_post = {4: {"title": "4 post", "content": "music post"}}
text_post = {5: {"title": "5 post", "content": "books post"}}
text_post = {6: {"title": "6 post", "content": "snickers post"}}
text_post = {7: {"title": "7 post", "content": "food post"}}
text_post = {8: {"title": "8 post", "content": "hobby post"}}
text_post = {9: {"title": "9 post", "content": "work post"}}


@app.get("/posts")
def get_all_posts():
    return text_post


@app.get("/post/{id}")
def get_all_posts(id: int):
    if id not in text_post:
        raise HTTPException(status_code=404, detail="❌ Post not found!")
    return text_post.get(id)
