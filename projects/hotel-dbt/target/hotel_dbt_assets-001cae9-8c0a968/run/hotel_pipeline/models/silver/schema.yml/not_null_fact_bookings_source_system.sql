
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select source_system
from "hotel"."main"."fact_bookings"
where source_system is null



  
  
      
    ) dbt_internal_test