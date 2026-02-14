import os
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator

# Path to the dbt project (mounted in Docker)
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "/app/dbt")

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

@dbt_assets(manifest=os.path.join(DBT_PROJECT_DIR, "target", "manifest.json"))
def hotel_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
