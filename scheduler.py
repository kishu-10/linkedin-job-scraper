from datetime import datetime, timedelta
from airflow import DAG
from core.helpers import save_data_to_csv
from core.linkedin import LinkedIn
from airflow.operators.python import PythonOperator


def schedule_job_task():
    try:
        linkedin = LinkedIn()
        jobs = linkedin.scrape_jobs("Nepal")
        save_data_to_csv(jobs)
    except Exception as e:
        raise ValueError(str(e))


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "job_scheduler_dag",
    default_args=default_args,
    description="To get Linkedin's job vacancies and save it in a csv file daily",
    schedule_interval=timedelta(days=1),
)

task = PythonOperator(
    task_id="my_task",
    python_callable=schedule_job_task,
    dag=dag,
)

if __name__ == "__main__":
    dag.cli()
