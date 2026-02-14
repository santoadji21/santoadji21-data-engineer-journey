SELECT 
    source_system,
    COUNT(*) as total_bookings,
    AVG(amount) as avg_revenue,
    MAX(ingestion_time) as last_updated
FROM {{ ref('fact_bookings') }}
GROUP BY 1
