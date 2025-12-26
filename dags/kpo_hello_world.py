from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


#TEST
with DAG(
    dag_id="kpo_hello_world",
    description="Simple KubernetesPodOperator test",
    start_date=datetime(2025, 1, 1),
    schedule=None,          # manual
    catchup=False,
    tags=["test", "kubernetes"],
) as dag:

    hello_k8s = KubernetesPodOperator(
        task_id="hello_from_k8s",
        name="hello-from-k8s",
        namespace="airflow",          # same airflow namespace!
        image="busybox:1.36",
        cmds=["sh", "-c"],
        arguments=["echo '🚀 Hello from KubernetesPodOperator!' && sleep 5"],
        get_logs=True,
        is_delete_operator_pod=True,  # clean up pod after run
    )

    hello_k8s
