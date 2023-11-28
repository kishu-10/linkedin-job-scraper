from decouple import config
import requests
from fastapi.responses import RedirectResponse
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp


class LinkedIn:
    LINKEDIN_URL = config("LINKEDIN_URL")
    CLIENT_ID = config("CLIENT_ID")
    CLIENT_SECRET = config("CLIENT_SECRET")
    REDIRECT_URI = config("REDIRECT_URI")
    SCOPE = "email"
    GRANT_TYPE = "authorization_code"

    @property
    def authorization_url(self):
        return f"{self.LINKEDIN_URL}oauth/v2/authorization"

    @property
    def access_token_url(self):
        return f"{self.LINKEDIN_URL}oauth/v2/accessToken"

    def authorization(self):
        params = {
            "response_type": "code",
            "client_id": self.CLIENT_ID,
            "redirect_uri": self.REDIRECT_URI,
            "scope": self.SCOPE,
        }
        response = requests.get(self.authorization_url, params=params)
        return RedirectResponse(response.url)

    def get_access_token(self, code):
        data = {
            "grant_type": self.GRANT_TYPE,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
        }
        response = requests.post(self.access_token_url, data=data)
        json_response = response.json()
        return json_response.get("access_token")

    def get_jobs(self, access_token):
        url = "https://api.linkedin.com/v2/simpleJobPostings"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.post(url, headers=headers)
            return response.json()
        except Exception as e:
            raise Exception("Failed to get access token")

    async def async_scrape_jobs(self, location):
        url = f"{self.LINKEDIN_URL}jobs/search"
        job_data_list = []
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._async_extract_job_data(session, url, location, start)
                for start in range(0, 200, 25)
            ]
            job_data_list = await asyncio.gather(*tasks)

        job_data_df = pd.concat(job_data_list)
        return job_data_df

    async def _async_extract_job_data(self, session, url, location, start):
        params = {
            "keywords": "",
            "location": location,
            "geoId": "",
            "trk": "public_jobs_jobs-search-bar_search-submit",
            "position": 1,
            "pageNum": 0,
            "start": start,
        }

        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), "html.parser")
                job_cards = soup.find_all("div", class_="base-search-card__info")
                return self._extract_job_data(job_cards)

        except Exception as e:
            print(str(e))
            return pd.DataFrame()

    def _extract_job_data(self, job_cards):
        job_list = []
        for job_card in job_cards:
            job_dict = {}
            title = job_card.find("h3", class_="base-search-card__title")
            job_dict["title"] = title.text.strip() if title else None

            company = job_card.find("h4", class_="base-search-card__subtitle")
            job_dict["company"] = company.text.strip() if company else None

            job_location = job_card.find("span", class_="job-search-card__location")
            job_dict["location"] = job_location.text.strip() if job_location else None

            published_date = job_card.find("time", class_="job-search-card__listdate")
            job_dict["published_date"] = (
                published_date.text.strip() if published_date else None
            )
            job_list.append(job_dict)
        return pd.DataFrame(job_list)
