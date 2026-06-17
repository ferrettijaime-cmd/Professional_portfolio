---FACT ORDERS---

CREATE TABLE analytics.fact_orders AS
SELECT
      o.order_id,
      o.customer_id,
      o.order_status,
      o.order_purchase_timestamp,
      o.order_approved_at,
      o.order_delivered_carrier,
      o.order_delivered_customer,
      o.order_estimated_delivery,

      COUNT(i.order_item_id) AS total_items,

      SUM(i.price) AS total_price,

      SUM(i.freight_value) AS total_freight,

      AVG(r.review_score) AS review_score

FROM staging.orders_clean o

LEFT JOIN staging.orders_items_clean i
       ON o.order_id = i.order_id

LEFT JOIN staging.orders_reviews_clean r
       ON o.order_id = r.order_id

GROUP BY
      o.order_id,
      o.customer_id,
      o.order_status,
      o.order_purchase_timestamp,
      o.order_approved_at,
      o.order_delivered_carrier,
      o.order_delivered_customer,
      o.order_estimated_delivery;

ALTER TABLE analytics.fact_orders
ADD PRIMARY KEY (order_id);

---DIM CUSTOMERS---

CREATE TABLE analytics.dim_customers AS
SELECT
      customer_id,
      customer_unique_id,
      customer_city,
      customer_state
FROM staging.customers_clean;

ALTER TABLE analytics.dim_customers
ADD PRIMARY KEY (customer_id);

--- DIM SELLERS---

CREATE TABLE analytics.dim_sellers AS
SELECT
      seller_id,
      seller_zip_code_prefix AS zip_code_prefix,
      seller_city,
      seller_state
FROM staging.sellers_clean;

ALTER TABLE analytics.dim_sellers
ADD PRIMARY KEY (seller_id);

---DIM PRODUCTS---

CREATE TABLE analytics.dim_products AS
SELECT
      product_id,
      product_category_name,
      product_name_lenght,
      product_description_lenght,
      product_photos_qty,
      product_weight_g,
      product_length_cm,
      product_height_cm,
      product_width_cm
FROM staging.products_clean;

ALTER TABLE analytics.dim_products
ADD PRIMARY KEY (product_id);

---DIM PRODUCT CATEGORY---

CREATE TABLE analytics.dim_product_category_name AS
SELECT
      product_category_name,
      product_category_name_english
FROM staging.product_category_name_clean;

ALTER TABLE analytics.dim_product_category_name
ADD PRIMARY KEY (product_category_name);

---DIM GEOLOCATION---

CREATE TABLE analytics.dim_geolocation AS
SELECT
      geolocation_zip_code_prefix AS zip_code_prefix,
      geolocation_lat,
      geolocation_lng,
      geolocation_city,
      geolocation_state
FROM staging.geolocation_clean;

---  FACT ORDER ITEMS---

CREATE TABLE analytics.fact_order_items AS
SELECT
      order_id,
      order_item_id,
      product_id,
      seller_id,
      shipping_limit_date,
      price,
      freight_value
FROM staging.orders_items_clean;

ALTER TABLE analytics.fact_order_items
ADD PRIMARY KEY (order_id, order_item_id);

--- FACT PAYMENTS---

CREATE TABLE analytics.fact_payments AS
SELECT
      order_id,
      payment_type,
      payment_installments,
      payment_value
FROM staging.orders_payments_clean;