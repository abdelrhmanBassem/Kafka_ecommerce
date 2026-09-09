CREATE VIEW Gold_transformation_task1 AS 
SELECT 
        customer_id,
        DATE(event_timestamp) AS event_date,
        sum(amount) as total_revenu,
        count_if(event_type='PURCHASE') AS PURCHASE_count
        FROM Kafka_DB.STREAMING.KAFKA_EVENTS_SILVER
        WHERE event_type='PURCHASE'
        GROUP BY customer_id,DATE(event_timestamp);

CREATE VIEW Gold_transformation_task2 AS 
SELECT 
    DATE(event_timestamp) AS event_date,
    count_if(event_type='PAGE_VIEW') AS page_view,
    count_if(event_type='ADD_TO_CART') AS add_to_cart,
    count_if(event_type='PURCHASE') AS purschase
     FROM Kafka_DB.STREAMING.KAFKA_EVENTS_SILVER
      GROUP BY DATE(event_timestamp);
    
    
