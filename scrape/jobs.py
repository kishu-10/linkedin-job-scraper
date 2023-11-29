from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


class LinkedInJobScraper:
    LINKEDIN_URL = config("LINKEDIN_URL")

    def get_web_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def __init__(self):
        self.driver = self.get_web_driver()

    def close_driver(self):
        self.driver.quit()

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

    def login_to_linkedin(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="m_login_email"]'))
        )
        email = self.driver.find_element(By.XPATH, '//*[@id="m_login_email"]')
        email.send_keys(self.email)
        password = self.driver.find_element(By.XPATH, '//*[@type="password"]')
        password.send_keys(self.password)
        button = self.driver.find_element(By.XPATH, '//*[@name="login"]')
        button.click()
        return self.driver

    def _check_if_scroll_btn_exists(self, driver):
        try:
            load_more_btn = driver.find_element(
                By.XPATH,
                "//button[@class='infinite-scroller__show-more-button infinite-scroller__show-more-button--visible']",
            )
            return load_more_btn
        except NoSuchElementException:
            return None

    def _scroll_down(self, driver):
        for _ in range(50):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if self._check_if_scroll_btn_exists(driver):
                self._check_if_scroll_btn_exists(driver).click()
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
        self.driver.get(self.job_search_url)
        self._scroll_down(self.driver)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="base-search-card__info")
        job_dataframe = self._extract_job_data(job_cards)
        return job_dataframe
