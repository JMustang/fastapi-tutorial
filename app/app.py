from fastapi import FastAPI, HTTPException

app = FastAPI()

text_post = {
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
        return list(text_post.values())[:limit]
    return text_post


@app.get("/post/{id}")
def get_all_posts(id: int):
    if id not in text_post:
        raise HTTPException(status_code=404, detail="❌ Post not found!")
    return text_post.get(id)
