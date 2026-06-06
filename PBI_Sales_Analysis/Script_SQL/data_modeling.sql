with sales_analysis as (
    select
        c.customer_city,
        count(distinct o.order_id) as total_orders,
        sum(o.price) as total_price,
        sum(o.freight_value) as total_freight_value,
        sum(o.price + o.freight_value) as total_paid
    from analytics.fact_orders o
    left join analytics.dim_customers c
        on c.customer_id = o.customer_id
    group by c.customer_city
)

select *
from sales_analysis



with payment_analysis as (
    select
        c.customer_city,
        p.payment_type,
        count(distinct o.order_id) as total_orders,
        row_number() over(
            partition by c.customer_city
            order by count(distinct o.order_id) desc
        ) as rn
    from analytics.fact_orders o
    join analytics.dim_customers c
        on c.customer_id = o.customer_id
    join analytics.fact_payments p
        on p.order_id = o.order_id
    group by c.customer_city, p.payment_type
)

select *
from payment_analysis
where rn = 1;


with category_analysis as (
    select
        c.customer_city,
        p.product_category_name,
        sum(oi.price) as total_sales,
        row_number() over(
            partition by c.customer_city
            order by sum(oi.price) desc
        ) as rn
    from analytics.fact_orders o
    join analytics.dim_customers c
        on c.customer_id = o.customer_id
    join analytics.fact_orders_items oi
        on oi.order_id = o.order_id
    join analytics.dim_products p
        on p.product_id = oi.product_id
    group by
        c.customer_city,
        p.product_category_name
)
select *
from category_analysis
where rn = 1;


      
      

      
      
      
      
      
      

    
      
      





