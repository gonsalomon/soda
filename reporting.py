import logging
from dataclasses import asdict, dataclass
import httpx
import pandas as pd
from decouple import config
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - [%(name)s %(funcName)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

API_MAIN_URL = "https://reporting.cloud.us.soda.io/v1/"
ENDPOINTS = {
    "dataset_health": "/quality/dataset_health",
    "datasets": "/coverage/datasets",
    "dataset_coverage": "/coverage/dataset_coverage",
}


@dataclass
class SnowflakeCredentials:
    account: str = config("account", default="kcaaaqb-lqa43598")
    user: str = config("user", default="GONSALOMON")
    password: str = config("password", default="Gon_123.")
    database: str = config("database", default="SODA_REPORTING_DB")
    schema: str = config("schema", default="PUBLIC")
    warehouse: str = config("warehouse", default="SODA_REPORTING")


@dataclass
class ApiAuth:
    soda_username: str = config("soda_username", default="gonzalo.salomon@weplan-latam.com")
    soda_password: str = config("soda_password", default="1234Weplan.")


def get_results(url: str, api_credentials: ApiAuth) -> pd.DataFrame:
    logger.info("Requesting data from: %s", url)
    request_result = httpx.post(
        url, auth=(api_credentials.soda_username, api_credentials.soda_password)
    )

    # check that the response is good. A good response comes with a 200 status code
    if request_result.status_code == 200:
        logger.info("Request successful")

        result_json = request_result.json().get("data", {})
        logger.debug(result_json)
        return pd.DataFrame.from_records(result_json)
    else:
        raise httpx.RequestError(f"{request_result.status_code=}, {request_result.json()=}")


def push_to_db(
    db_credentials: SnowflakeCredentials,
    df: pd.DataFrame,
    qualified_target_table_name: str,
    if_exists: str = "replace",
) -> None:
    db_url_string = URL(**asdict(db_credentials))
    sql_engine = create_engine(db_url_string)
    logger.info("Pushing data to %s", qualified_target_table_name)
    # We used a csv in case Snowflake wasn't working
    df.to_csv('dataset.csv', index=False)
    df.to_sql(qualified_target_table_name, con=sql_engine, if_exists=if_exists, index=False)
    logger.info("Data successfully pushed to %s", qualified_target_table_name)


def main():
    api_credentials = ApiAuth()
    datasets = get_results(f"{API_MAIN_URL}{ENDPOINTS['datasets']}", api_credentials)

    # convert the `tags` column from a list to a comma separated string to play well with SQL later
    datasets["tags"] = datasets["tags"].str.join(",")

    dataset_health = get_results(f"{API_MAIN_URL}{ENDPOINTS['dataset_health']}", api_credentials)

    push_to_db(SnowflakeCredentials(), datasets, "datasets_report")

    push_to_db(SnowflakeCredentials(), dataset_health, "dataset_health_report")


if __name__ == "__main__":
    main()