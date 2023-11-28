from fastapi import Depends, FastAPI, HTTPException, Request, status

from core.helpers import save_data_to_csv
from core.utils import Response
from .linkedin import LinkedIn
from fastapi.encoders import jsonable_encoder

api_app = FastAPI()


@api_app.get("/")
def index():
    return {"message": "This is v1 of this application."}


@api_app.get("/linkedin/authorization")
async def linkedin_authorization(linkedin: LinkedIn = Depends()):
    return linkedin.authorization()


@api_app.get("/linkedin/access-token")
async def linkedin_access_token(
    request: Request, code: str, linkedin: LinkedIn = Depends()
):
    try:
        access_token = linkedin.get_access_token(code)
        request.session["access_token"] = access_token
        return access_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@api_app.get("/linkedin/jobs")
async def linkedin_jobs(request: Request, linkedin: LinkedIn = Depends()):
    try:
        access_token = request.session.get("access_token")
        jobs = linkedin.get_jobs(access_token)
        return jobs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@api_app.get("/linkedin/get-jobs")
async def linkedin_scrape_jobs(location: str = "Nepal", linkedin: LinkedIn = Depends()):
    try:
        jobs = await linkedin.async_scrape_jobs(location)
        save_data_to_csv(jobs)
        return Response(status.HTTP_200_OK, "Job data retrieved successfully", {})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
