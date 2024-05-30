import logging 
from datetime import datetime  

from airflow import DAG 
from airflow.models import Variable 
from airflow.hooks.base_hook import BaseHook 
from airflow.operators.python_operator import PythonOperator


def get_secrets(**kwargs):    
    # Test connections   
    conn = BaseHook.get_connection(kwargs['my_conn_id'])
    logging.info(
        f"Password: {conn.password}, Login: {conn.login}, "
        f"URI: {conn.get_uri()}, Host: {conn.host}"
    )

    # Test variables     
    test_var = Variable.get(kwargs['var_name'])
    logging.info(f'my_var_name: {test_var}')


with DAG(   
    'test_vault_connection',    
    start_date=datetime(2020, 1, 1),    
) as dag:      
    test_task = PythonOperator(         
        task_id='test-task',         
        python_callable=get_secrets,         
        op_kwargs={
            'my_conn_id': 'connection_to_test',
            'var_name': 'my_test_var',
        },     
    )
