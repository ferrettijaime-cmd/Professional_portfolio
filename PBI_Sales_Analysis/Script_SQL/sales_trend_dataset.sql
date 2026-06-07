---How much, where, and when do we sell?---

with sales_analysis as (
    select
        o.order_purchase_timestamp::date as date,
        c.customer_city,
        count(distinct o.order_id) as total_orders,
        sum(o.price) as total_price,
        sum(o.freight_value) as total_freight_value,
        sum(o.price + o.freight_value) as total_paid
    from analytics.fact_orders o
    left join analytics.dim_customers c
        on c.customer_id = o.customer_id
    group by
        o.order_purchase_timestamp::date,
        c.customer_city
)
select *
from sales_analysis

    



      
