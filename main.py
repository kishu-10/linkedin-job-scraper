from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.api import api
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(SessionMiddleware, secret_key="Foo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", api)


@app.get("/")
async def main():
    return {"message": "Hello World"}
