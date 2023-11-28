from decouple import config
import requests
from fastapi.responses import RedirectResponse
from bs4 import BeautifulSoup


class LinkedIn:
    client_id = config("CLIENT_ID")
    client_secret = config("CLIENT_SECRET")
    redirect_uri = config("REDIRECT_URI")
    grant_type = "authorization_code"
    linkedin_url = config("LINKEDIN_URL")

    def authorization(self):
        url = "https://www.linkedin.com/oauth/v2/authorization"
        _params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "email",
        }
        response = requests.get(url, params=_params)
        return RedirectResponse(response.url)

    def get_access_token(self, code):
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        content_type = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(url, data=body, headers=content_type)
        return response.json()["access_token"]

    def get_jobs(self, access_token):
        url = "https://api.linkedin.com/v2/simpleJobPostings"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, headers=headers)
        return response.json()["message"]

    def scrape_jobs(self, location="Nepal"):
        _url = f"{self.linkedin_url}jobs/search"
        _params = {
            "keywords": "",
            "location": location,
            "geoId": "",
            "trk": "public_jobs_jobs-search-bar_search-submit",
            "position": 1,
            "pageNum": 0,
        }
        response = requests.get(_url, params=_params)
        soup = BeautifulSoup(response.content, "html.parser")
        job_cards = soup.find_all("div", class_="base-search-card__info")
        job_list = []

        for job_card in job_cards:
            job_dict = {}

            title = job_card.find("h3", class_="base-search-card__title")
            job_dict["title"] = title.text.strip() if title else None

            company = job_card.find("h4", class_="base-search-card__subtitle")
            job_dict["company"] = company.text.strip() if company else None

            job_location = job_card.find("span", class_="job-search-card__location")
            job_dict["location"] = job_location.text.strip() if job_location else None

            benefits = job_card.find("span", class_="result-benefits__text")
            job_dict["benefits"] = benefits.text.strip() if benefits else None

            published_date = job_card.find("time", class_="job-search-card__listdate")
            job_dict["published_date"] = (
                published_date.text.strip() if published_date else None
            )

            job_list.append(job_dict)

        return job_list
