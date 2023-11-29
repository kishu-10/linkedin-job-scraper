from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


class LinkedInJobScraper:
    LINKEDIN_URL = config("LINKEDIN_URL")

    @property
    def login_url(self):
        return f"{self.LINKEDIN_URL}login"

    @property
    def job_search_url(self):
        params = {
            "location": "Nepal",
            "geoId": 104630404,
            "trk": "public_jobs_jobs-search-bar_search-submit",
        }
        param_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{self.LINKEDIN_URL}jobs/search?{param_string}"

    def get_web_driver(self):
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def login_facebook(self):
        driver = self.get_web_driver()
        driver.get(self.login_url)
        email = driver.find_element(By.XPATH, '//*[@id="m_login_email"]')
        email.send_keys(self.email)
        password = driver.find_element(By.XPATH, '//*[@type="password"]')
        password.send_keys(self.password)
        button = driver.find_element(By.XPATH, '//*[@name="login"]')
        button.click()
        time.sleep(5)
        driver.get(f"{self.LINKEDIN_URL}/jobs/search")
        time.sleep(4)
        return driver

    def _scroll_down(self, driver):
        for _ in range(5):
            _body = driver.find_element(By.TAG_NAME, "body")
            _body.send_keys(Keys.END)
            time.sleep(2)

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

    def get_jobs(self):
        driver = self.get_web_driver()
        driver.get(self.job_search_url)
        self._scroll_down(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="base-search-card__info")
        job_dataframe = self._extract_job_data(job_cards)
        return job_dataframe
