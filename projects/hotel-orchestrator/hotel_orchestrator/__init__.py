from dagster import Definitions, load_assets_from_modules
from . import assets
from .schedules import every_minute_schedule
from dagster_dbt import DbtCliResource
import os

DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "/app/dbt")

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    schedules=[every_minute_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
    },
)
