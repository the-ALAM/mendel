from airflow.models import DagBag # type: ignore

def get_all_dags():
    dagbag = DagBag()
    dagbag.collect_dags_from_db()

    all_dags = []
    for dag_id, dag in dagbag.dags.items():
        all_dags.append(dag)

    return all_dags

if __name__ == '__main__':
    dags = get_all_dags()
    for dag in dags:
        print(dag.dag_id)
