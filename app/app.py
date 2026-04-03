from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def Hello():
    return {"message": "🖖🏻 Hello dev!"}
