from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from process.crypto_monitor import main


default_args = {
    "owner": "airflow"
}

dag_init = DAG(
    "ingest_crypto_data",
    description="Extract, clean and load crypto data from CoinGecko API.",
    start_date=datetime(2022, 10, 1),
    default_args=default_args,
    tags=["Ingest", "Crypto", "CoinGecko", "API"],
    schedule_interval="@daily"
    )


with dag_init as dag:
    exchanges_task = PythonOperator(
        task_id="create_exchanges_tables", 
        python_callable=main
    )

    exchanges_task 