## Installation

Create and activate virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Setup .env file

```sh
CLIENT_ID="Foo"
CLIENT_SECRET="Foo"
REDIRECT_URI="Foo"
RECOMMENDED_JOBS_URL="https://www.linkedin.com/jobs/collections/recommended"
SEARCH_JOBS_URL="https://www.linkedin.com/jobs/search/"
LINKEDIN_URL="https://www.linkedin.com/"
```

Start the FastAPI server:

```sh
uvicorn main:app --reload
```

## For Scheduling Task in Apache Airflow

Create an admin user to access Airflow Web UI:

```sh
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@admin.com
```

Start the Airflow scheduler to run DAG:

```sh
airflow scheduler
```

To access Airflow Web UI:

```sh
airflow webserver -p 8080
```
