from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_hello_world', default_args=default_args, schedule_interval=timedelta(minutes=10))


start = DummyOperator(task_id='start', dag=dag)

passing = KubernetesPodOperator(namespace='default',
                          image="python:3.6",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          annotations= { "vault.hashicorp.com/agent-inject": "true",
                                          "vault.hashicorp.com/tls-skip-verify": "true",
                                          "vault.hashicorp.com/role": "basic-secret-role",
                                        "vault.hashicorp.com/agent-inject-secret-helloworld": "secret/basic-secret/helloworld",
                                        "vault.hashicorp.com/agent-inject-template-helloworld": '''{{- with secret "secret/basic-secret/helloworld" -}}"
                                            {{ .Data.data | toJSON}}
                                        
                                        {{ end }}'''
                                        }
                          labels={"foo": "bar"},
                          name="passing-test",
                          task_id="passing-task",
                          get_logs=True,
                          dag=dag
                          )

                          

end = DummyOperator(task_id='end', dag=dag)


passing.set_upstream(start)
passing.set_downstream(end)
