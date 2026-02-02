import datetime

from airflow.providers.standard.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow import DAG
from airflow.sdk import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook


def twelvedata_api_key() -> str:
    return Variable.get("twelvedata_api_key")


def get_data(td_api_key, logical_date) -> dict:
    from twelvedata import TDClient

    td = TDClient(apikey=td_api_key)

    ts = td.exchange_rate(symbol="USD/EUR", date=logical_date.isoformat())
    data = ts.as_json()
    return data


def save_data(data: dict) -> None:
    print("Saving the data to db postgres_storage")

    if not data:
        raise ValueError("No data received")

    pg_hook = PostgresHook(postgres_conn_id="postgres_storage")

    insert_sql = """
                 INSERT INTO exchange_rates (symbol, rate, created_at)
                 VALUES (%s, %s, %s); \
                 """

    symbol = data["symbol"]
    rate = data["rate"]
    timestamp = datetime.datetime.fromtimestamp(data["timestamp"])

    pg_hook.run(insert_sql, parameters=(symbol, rate, timestamp))
    print("Data inserted into Postgres!")

with DAG(
        dag_id="connections_and_variables",
        schedule=datetime.timedelta(minutes=1),
        tags={"exercise_5"},
    ) as dag:

    get_api_key_op = PythonOperator(
        task_id="get_twelvedata_api_key",
        python_callable=twelvedata_api_key,
    )

    get_data_op = PythonVirtualenvOperator(task_id="get_data", python_callable=get_data,
                                           requirements=["twelvedata", "pendulum", "lazy_object_proxy"],
                                           serializer="cloudpickle",
                                           op_kwargs={"td_api_key": get_api_key_op.output})
    save_data_op = PythonOperator(
        task_id="save_data",
        python_callable=save_data,
        op_kwargs={"data": get_data_op.output},
    )

    get_api_key_op >> get_data_op >> save_data_op
