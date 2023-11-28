from fastapi import FastAPI, Request
from .linkedin import LinkedIn

api = FastAPI()


@api.get("/")
def index():
    return {"message": "This is v1 of this application."}


@api.get("/linkedin/authorization")
async def linkedin_authorization():
    linkedin = LinkedIn()
    return linkedin.authorization()


@api.get("/linkedin/access-token")
async def linkedin_access_token(request: Request):
    _code = request.query_params.get("code")
    linkedin = LinkedIn()
    access_token = linkedin.get_access_token(_code)
    request.session["access_token"] = access_token
    return access_token


@api.get("/linkedin/jobs")
async def linkedin_jobs(request: Request):
    linkedin = LinkedIn()
    access_token = request.session.get("access_token")
    return linkedin.get_jobs(access_token)

@api.get("/linkedin/scrape-jobs")
async def linkedin_jobs():
    linkedin = LinkedIn()
    return linkedin.scrape_jobs()
