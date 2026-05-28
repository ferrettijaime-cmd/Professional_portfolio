with order_level as (

select
    o.order_id,
    o.customer_id,
    c.customer_state,

    sum(oi.price) as total_price,
    sum(oi.freight_value) as total_freight,

    sum(oi.price + oi.freight_value) as total_paid_items,

    max(p.payment_value) as payment_value,

    max(p.payment_installments) as payment_installments,

    o.order_purchase_timestamp::date,
    o.delivery_delay_days,
    o.review_score

from analytics.fact_orders o

left join analytics.fact_orders_items oi
     on oi.order_id = o.order_id

left join analytics.fact_payments p
     on p.order_id = o.order_id

left join analytics.dim_customers c
     on c.customer_id = o.customer_id

group by
    o.order_id,
    o.customer_id,
    c.customer_state,
    o.order_purchase_timestamp::date,
    o.delivery_delay_days,
    o.review_score
),
customer_level as (

select
    customer_id,
    
    avg(total_paid_items) as avg_order_value,
    
    max(customer_state) as customer_state,

    count(distinct order_id) as total_orders,

    sum(payment_value) as total_spent,
    
    avg(payment_installments) as avg_payment_installments,

    avg(review_score) as avg_review_score,

    avg(delivery_delay_days) as avg_delivery_delay_days,

    max(order_purchase_timestamp::date) as last_purchase,

    min(order_purchase_timestamp::date) as first_purchase,
    
    (max(order_purchase_timestamp::date)
    - min(order_purchase_timestamp::date)) as customer_lifetime_days
   
from order_level

group by customer_id
),
customer_dataset as (
select 
     cl.*,
     (
      (select
           max(order_purchase_timestamp::date)
       from
           order_level) - cl.last_purchase) as recency_days
from customer_level cl ),
final_dataset as (
select 
      cd.*,
      case
         when
            recency_days > 180 then 1
         else 0
      end as churn_flag
from
    customer_dataset cd
)
select *
from final_dataset
    

      