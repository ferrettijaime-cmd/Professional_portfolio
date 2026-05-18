drop table if exists analytics.fact_orders;
create table analytics.fact_orders as
select
     o.order_id,
     o.customer_id,
     o.order_status,
     o.order_purchase_timestamp,
     o.order_approved_at,
     o.order_delivered_carrier,
     o.order_delivered_customer,
     o.order_estimated_delivery,
     i.order_item_id,
     i.price,
     i.seller_id,
     i.freight_value,
     r.review_score
from staging.orders_clean o
left join staging.orders_items_clean i on o.order_id = i.order_id
left join staging.orders_reviews_clean r on o.order_id = r.order_id;

alter table analytics.fact_orders
add primary key (order_id, order_item_id);



drop table if exists analytics.fact_payments;
create table analytics.fact_orders as
select
      p.payment_type,
     p.payment_installments,
     p.payment_value,
     r.review_score 
