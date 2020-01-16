"""
import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
"""
from datetime import datetime, timedelta

concurrency = 2
catchup = False

config = {
    'dag_id_1': {'schedule_interval': timedelta(minutes=15), "start_date": datetime.fromisoformat('2020-01-16'), "max_active_runs": 1},
    'dag_id_2': {'schedule_interval': timedelta(minutes=20), "start_date": datetime.fromisoformat('2020-01-16'), "max_active_runs": 1},
    'dag_id_3': {'schedule_interval': timedelta(minutes=25), "start_date": datetime.fromisoformat('2020-01-16'), "max_active_runs": 1}
}




for dict in config:
    print("%s" % dict)
"""
    with DAG(dag_id=dict.dag_id,
             schedule_interval=dict.schedule_interval,
             start_date=dict.start_date,
             max_active_runs=dict.max_active_runs,
             concurrency=concurrency,
             catchup=catchup
             ) as dag:
        DummyOperator(task_id='dummy-task',dag=dag)

"""
