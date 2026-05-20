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
left join (select order_id,
     avg(review_score) as review_score
     from staging.orders_reviews_clean
     group by order_id) r on o.order_id = r.order_id
where
     i.order_item_id is not null;

alter table analytics.fact_orders
add primary key (order_id, order_item_id);

drop table if exists analytics.fact_payments;
create table analytics.fact_payments as
select
     order_id,
     payment_type,
     payment_installments,
     payment_value
from
    staging.orders_payments_clean;

drop table if exists analytics.dim_customers;
create table analytics.dim_customers as 
select
      customer_id,
      customer_unique_id,
      customer_city,
      customer_state
from
    staging.customers_clean;

alter table analytics.dim_customers
add primary key (customer_id);

drop table if exists analytics.dim_sellers;
create table analytics.dim_sellers as 
select
      seller_id,
      seller_zip_code_prefix as zip_code_prefix,
      seller_city,
      seller_state
from
    staging.sellers_clean;

alter table analytics.dim_sellers
add primary key (seller_id);

drop table if exists analytics.dim_geolocation;
create table analytics.dim_geolocation as 
select
      geolocation_zip_code_prefix as zip_code_prefix,
      geolocation_lat,
      geolocation_lng,
      geolocation_city,
      geolocation_state
from
    staging.geolocation_clean;

drop table if exists analytics.dim_products;
create table analytics.dim_products as 
select
      p.product_id,
      p.product_category_name
from
    staging.products_clean;

alter table analytics.dim_products
add primary key(product_id);

drop table if exists analytics.fact_orders_items;
create table analytics.fact_orders_items as 
select
      order_id,
      order_item_id,
      product_id,
      seller_id,
      shipping_limit_date,
      price,
      freight_value
from
    staging.orders_items_clean;

alter table analytics.fact_orders_items 
add primary key (order_id, order_item_id);

alter table analytics.fact_orders_items
add constraint fk_seller_id
foreign key (seller_id)
references analytics.dim_sellers(seller_id);

alter table analytics.fact_orders_items
add constraint fk_product_id
foreign key (product_id)
references analytics.dim_products(product_id);

drop table if exists analytics.dim_product_category_name;
create table analytics.dim_product_category_name as
select
      product_category_name,
      product_category_name_english
from
    staging.product_category_name_clean