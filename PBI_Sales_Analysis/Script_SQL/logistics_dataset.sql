--What is the volume of items shipped?, During what period are the most orders received?---
---What is the approval time?, How long does it take the delivery person to deliver a package?---
---Delivery efficiency---
with logistics_dataset as (
select
      o.order_purchase_timestamp::date as purchase_date,
      c.customer_city,
      count(distinct o.order_id) as total_orders,
      count(*) as total_items,
      sum(o.freight_value) as total_freight_value,
      avg(
          o.order_approved_at::date
          - o.order_purchase_timestamp::date
      ) as avg_approval_time,

      avg(
      	  case
      	  	  when
      	  	      o.order_delivered_customer is not null
      	  	  and o.order_delivered_carrier is not null
      	  	  then
      	  	      o.order_delivered_customer::date
          		  - o.order_delivered_carrier::date
      	  end
      ) as avg_time_on_route,
      avg(o.delivery_delay_days) as avg_delivery_delay
from analytics.fact_orders o
left join analytics.dim_customers c
    on o.customer_id = c.customer_id
group by
    o.order_purchase_timestamp::date,
    c.customer_city
)
select *
from  logistics_dataset
where  avg_delivery_delay is not null
and    avg_approval_time is not null

      

      
      