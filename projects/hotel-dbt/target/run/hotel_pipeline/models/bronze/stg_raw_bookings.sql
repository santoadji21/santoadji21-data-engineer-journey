
  
  create view "hotel"."main"."stg_raw_bookings__dbt_tmp" as (
    SELECT * FROM '/app/data/raw/*.parquet'
  );
