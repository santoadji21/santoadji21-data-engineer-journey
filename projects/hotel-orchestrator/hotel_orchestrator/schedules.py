from dagster import ScheduleDefinition, define_asset_job, AssetSelection

# define_asset_job() creates a job that materializes selected assets
# AssetSelection.all() selects all assets in the project
run_everything_job = define_asset_job(
    name="run_everything_job",
    selection=AssetSelection.all()
)

# ScheduleDefinition creates a cron-based schedule
# cron_schedule="* * * * *" runs every minute
every_minute_schedule = ScheduleDefinition(
    job=run_everything_job,
    cron_schedule="* * * * *",
)
