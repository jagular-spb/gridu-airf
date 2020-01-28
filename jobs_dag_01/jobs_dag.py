import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

concurrency = 2
catchup = False

config = {
    'dag_id_1': {'schedule_interval': timedelta(minutes=45), 'start_date': datetime(2020, 1, 18), 'max_active_runs': 2,
                 "table_name": "table_num_1"},
    'dag_id_2': {'schedule_interval': timedelta(minutes=40), 'start_date': airflow.utils.dates.days_ago(1),
                 'max_active_runs': 3, "table_name": "table_num_2"},
    'dag_id_3': {'schedule_interval': timedelta(minutes=55), 'start_date': airflow.utils.dates.days_ago(1),
                 'max_active_runs': 1, "table_name": "table_num_3"}
}


def print_to_log(**kwargs):

    pprint(kwargs)
    dag_id = kwargs['dag_id']
    database = kwargs['database']
    print(" %s start processing tables in database: %s" % (dag_id, database))
    return 'Whatever you return gets printed in the logs'


for dict in config:
    args = {
        'owner': 'airflow',
        'start_date': config[dict]['start_date'],
        'max_active_runs': config[dict]['max_active_runs'],
        'dagrun_timeout': timedelta(minutes=10),
        'concurrency': concurrency,
        'catchup': catchup,
        'database': 'our_test_db'
    }
    with DAG(dag_id=dict, default_args=args, schedule_interval=config[dict]['schedule_interval']) as dag:

        dop0 = PythonOperator(task_id='python-task-' + dict,
                              provide_context=True,
                              python_callable=print_to_log
                              )

        dop1 = BashOperator(task_id='dummy-sub-task-' + dict, bash_command='echo `date`')
        dop1.set_upstream(dop0)

    if dag:
        globals()[dict] = dag
else:
    print("Finished")

""" test 2 """
