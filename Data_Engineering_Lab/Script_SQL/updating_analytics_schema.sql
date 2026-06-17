
---fact_orders---

truncate table analytics.fact_payments cascade;
truncate table analytics.fact_order_items cascade;
truncate table analytics.fact_orders cascade;

insert into analytics.fact_orders
(
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier,
    order_delivered_customer,
    order_estimated_delivery,
    total_items,
    total_price,
    total_freight,
    review_score
)
select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier,
    o.order_delivered_customer,
    o.order_estimated_delivery,
    count(i.order_item_id) as total_items,
    sum(i.price) as total_price,
    sum(i.freight_value) as total_freight,
    avg(r.review_score) as review_score
from staging.orders_clean o
left join staging.orders_items_clean i
    on o.order_id = i.order_id
left join staging.orders_reviews_clean r
    on o.order_id = r.order_id
group by
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier,
    o.order_delivered_customer,
    o.order_estimated_delivery;

   ---fact_order_items---
 
insert into analytics.fact_order_items
(
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value
)
select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value
from staging.orders_items_clean;

---fact_payments---

insert into analytics.fact_payments
(
    order_id,
    payment_type,
    payment_installments,
    payment_value
)
select
    order_id,
    payment_type,
    payment_installments,
    payment_value
from staging.orders_payments_clean;

---dim_customers---

truncate table analytics.dim_customers cascade;

insert into analytics.dim_customers
(
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
)
select
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
from staging.customers_clean;

---dim_sellers---

truncate table analytics.dim_sellers cascade;

insert into analytics.dim_sellers
(
    seller_id,
    zip_code_prefix,
    seller_city,
    seller_state
)
select
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
from staging.sellers_clean;

---dim_products---

truncate table analytics.dim_products cascade;

insert into analytics.dim_products
(
    product_id,
    product_category_name,
    product_name_lenght,
    product_description_lenght,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
select
    product_id,
    product_category_name,
    product_name_lenght,
    product_description_lenght,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
from staging.products_clean;

---dim_product_category_name---

truncate table analytics.dim_product_category_name cascade;

insert into analytics.dim_product_category_name
(
    product_category_name,
    product_category_name_english
)
select
    product_category_name,
    product_category_name_english
from staging.product_category_name_clean;

---dim_geolocation---

truncate table analytics.dim_geolocation;

insert into analytics.dim_geolocation
(
    zip_code_prefix,
    geolocation_lat,
    geolocation_lng,
    geolocation_city,
    geolocation_state
)
select
    geolocation_zip_code_prefix,
    geolocation_lat,
    geolocation_lng,
    geolocation_city,
    geolocation_state
from staging.geolocation_clean;