from decouple import config
import requests
from fastapi.responses import RedirectResponse


class LinkedIn:
    client_id = config("CLIENT_ID")
    client_secret = config("CLIENT_SECRET")
    redirect_uri = config("REDIRECT_URI")
    grant_type = "authorization_code"

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
