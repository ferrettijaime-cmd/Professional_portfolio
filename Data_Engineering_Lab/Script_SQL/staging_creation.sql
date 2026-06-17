drop table if exists staging.orders_clean;
    create table staging.orders_clean as
	select 
	      order_id,
	      customer_id,
	      order_status,
	      cast(order_purchase_timestamp as timestamp) as order_purchase_timestamp,
	      cast(order_approved_at as timestamp) as order_approved_at,
	      cast(order_delivered_carrier_date as timestamp) as order_delivered_carrier,
	      cast(order_delivered_customer_date as timestamp) as order_delivered_customer,
	      cast(order_estimated_delivery_date as timestamp) as order_estimated_delivery
	 from
	     raw.olist_orders_dataset;
	     
	drop table if exists staging.customers_clean;
    create table staging.customers_clean as 
	select
	      customer_id,
	      customer_unique_id,
          customer_zip_code_prefix,
	      customer_city,
	      customer_state
	from 
	    raw.olist_customers_dataset;
	 
	drop table if exists staging.orders_items_clean;
	create table staging.orders_items_clean as
	select 
	      order_id,
	      order_item_id,
	      product_id,
	      seller_id,
	      cast(shipping_limit_date as timestamp) as shipping_limit_date,
	      cast(price as numeric) as price,
	      cast(freight_value as numeric) as freight_value
	from 
	    raw.olist_orders_items_dataset;
	
	drop table if exists staging.orders_payments_clean;
	create table staging.orders_payments_clean as  
	select 
	      order_id,
	      payment_type,
	      payment_installments,
	      payment_value
	from
	    raw.olist_orders_payments_dataset;
	
	drop table if exists staging.orders_reviews_clean; 
	create table staging.orders_reviews_clean as
	select
	      review_id,
	      order_id,
	      review_score,
	      review_comment_title,
	      review_comment_message,
	      cast(review_creation_date as timestamp) as review_creation_date,
	      cast(review_answer_timestamp as timestamp) as review_answer_timestamp
	from
	    raw.olist_orders_reviews_dataset;
	  
	drop table if exists staging.products_clean;
	create table staging.products_clean as
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
	from
	    raw.olist_products_dataset;
	
	drop table if exists staging.geolocation_clean; 
	create table staging.geolocation_clean as
	select
	      geolocation_zip_code_prefix,
	      geolocation_lat,
	      geolocation_lng,
	      geolocation_city,
	      geolocation_state
	from 
	    raw.olist_geolocation_dataset;
	
	drop table if exists staging.sellers_clean; 
	create table staging.sellers_clean as 
	select
	      seller_id,
	      seller_zip_code_prefix,
	      seller_city,
	      seller_state
	from
	    raw.olist_sellers_dataset;
	
	drop table if exists staging.product_category_name_clean;
	create table staging.product_category_name_clean as 
	select
	      product_category_name,
	      product_category_name_english
	from
	    raw.product_category_name_translation;