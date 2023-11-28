from fastapi import FastAPI
from core.api import api_app
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="Foo")

app.mount("/api", api_app)


@app.get("/")
async def main():
    return {"message": "Hello World"}
