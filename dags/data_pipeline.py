
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

from airflow import DAG

from utils.config_manager import ConfigManager
from utils.dag_factory import register_dag


config_manager = ConfigManager()

def process_data_pipeline():
    print("Processing data pipeline...")


def create_dag(dag_id, config):
    # ------------------
    # DAG definition
    # ------------------
    with (DAG(
            dag_id=dag_id,
            start_date=datetime(2026, 2, 1),
            schedule_interval=config['schedule_interval'],
            catchup=False,  # This flag should be False to prevent backfilling from start_date
            default_args={"owner": "story-kraft"},
            tags=[config.get("env")],
            max_active_runs=1,
    ) as data_pipeline_dag):

        task = PythonOperator(
            task_id="process_task",
            python_callable=process_data_pipeline,
        )

        return data_pipeline_dag


register_dag("data_pipeline_dag", create_dag, config_manager.load_config)
