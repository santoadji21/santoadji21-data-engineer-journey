
  
    
    

    create  table
      "hotel"."main"."fact_bookings__dbt_tmp"
  
    as (
      WITH raw_data AS (
    SELECT * FROM "hotel"."main"."stg_raw_bookings"
)

SELECT 
    -- Determine Source System
    json_extract_string(raw_data, '$.source') as source_system,
    
    -- Normalize Guest Name
    COALESCE(
        json_extract_string(raw_data, '$.GUEST_NM'),       -- Legacy
        json_extract_string(raw_data, '$.guest.lastName'), -- Modern
        json_extract_string(raw_data, '$.client')          -- Budget
    ) as guest_name,
    
    -- Normalize Check-in Date
    COALESCE(
        json_extract_string(raw_data, '$.ARR_DT'),            -- Legacy
        json_extract_string(raw_data, '$.booking.checkInDate'), -- Modern
        json_extract_string(raw_data, '$.start_date')         -- Budget
    ) as check_in_date,
    
    -- Normalize Amount
    CAST(COALESCE(
        json_extract_string(raw_data, '$.AMT'),
        json_extract_string(raw_data, '$.booking.totalPrice'),
        json_extract_string(raw_data, '$.cost')
    ) AS DOUBLE) as amount,
    
    ingestion_time

FROM raw_data
    );
  
  