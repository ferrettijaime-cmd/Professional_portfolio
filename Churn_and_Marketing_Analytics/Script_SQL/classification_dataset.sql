with order_level as (

select
    c.customer_unique_id,
    c.customer_state,

    sum(o.price) as total_price,
    sum(o.freight_value) as total_freight,

    sum(o.price + o.freight_value) as total_paid_items,

    avg(p.payment_installments) as payment_installments,
    
    count(distinct o.order_id) as total_orders,

    max(o.order_purchase_timestamp::date) as last_purchase,
     min(o.order_purchase_timestamp::date) as first_purchase,
    (max(o.order_purchase_timestamp::date)
    - min(o.order_purchase_timestamp::date)) as customer_lifetime_days

from
    analytics.fact_orders o
left join 
         analytics.dim_customers c
         on c.customer_id = o.customer_id
left join
         analytics.fact_payments p
         on p.order_id = o.order_id

group by
        c.customer_unique_id,
    	c.customer_state
),
client_dataset as(
select
      ol.*,
      (total_paid_items/total_orders) as avg_order_value,
      (
       (select
             max(last_purchase)
       	from
           order_level) - ol.last_purchase) as recency_days
from
    order_level ol
)
select *
from
    client_dataset
    