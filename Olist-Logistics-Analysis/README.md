# Evaluation of Delivery SLA Compliance

## Project Overview

This project evaluates whether Olist's logistics operation is meeting its promised delivery deadlines. The analysis focuses on delivery performance, service-level agreement (SLA) compliance, and delivery timing relative to the estimated delivery date provided to customers.

The objective is not only to identify delivery delays but also to assess the overall effectiveness of the fulfillment process and understand whether delivery estimates are aligned with actual operational performance.

## Business Question

### *Are delivery deadlines being met according to the delivery commitments made to customers?*

To answer this question, the analysis examines:
- Order approval time
- Shipping preparation time
- Delivery performance relative to the estimated delivery date
- Overall On-Time Delivery Rate (OTD)

## Dataset
Source: Olist E-commerce Dataset

The analysis uses order-level logistics information stored in PostgreSQL and transformed through SQL queries.

## Variables

| Variable | Description |
|----------|-------------|
| purchase_time | Days between order purchase and order approval |
| shipping_time | Days between order approval and carrier pickup |
| delivery_delay_days | Difference between actual delivery date and estimated delivery date |

## Formula

delivery_delay_days =
actual_delivery_date - estimated_delivery_date

## Interpretation:

- Negative values → Early delivery
- Zero → On-time delivery
- Positive values → Late delivery

## Methodology

1. Extract logistics data from PostgreSQL.
2. Create delivery performance metrics using SQL.
3. Perform Exploratory Data Analysis (EDA).
4. Evaluate delivery time distributions.
5. Identify potential anomalies and outliers.
6. Calculate On-Time Delivery Rate (OTD).
7. Assess overall SLA compliance.

## Exploratory Data Analysis

### Descriptive Statistics

| Metric | Delivery Delay (days) |
|--------|-----------------------|
| Mean | -12.03 |
| Median | -13 |
| Std Dev | 10.16 |
| Minimum | -147 |
| Maximum | 188 |

## Key observations:

- Deliveries occur on average 12 days before the estimated delivery date.
- Mean and median are very similar, indicating a stable distribution.
- Extreme delays exist but represent a small proportion of orders.

## Delivery Distribution

The delivery delay distribution shows a strong concentration of observations before zero, indicating that most orders are delivered ahead of schedule.

The histogram confirms that late deliveries are relatively uncommon compared to early deliveries.

![Histogram_late_delivery](Images\late_delivery_distr.png)

## Outlier Analysis

A small number of extreme observations were identified through boxplot analysis.

Although some deliveries experienced significant delays, these cases did not materially affect the overall delivery performance metrics.

![Outliers_V](Images\outliers_values.png)

## On-Time Delivery Rate (OTD)

The main KPI used in this analysis is the On-Time Delivery Rate:

*OTD = Deliveries on or before estimated date / Total Deliveries*

Result ----> OTD = 93.4%
This indicates that approximately 93 out of every 100 orders were delivered on time or earlier than promised.

## Key Findings

- Olist achieved an On-Time Delivery Rate of 93.4%.
- Deliveries occurred approximately 12 days earlier than estimated on average.
- Shipping and approval processes showed low average processing times.
- Outliers were present but had minimal impact on overall delivery performance.
- No significant evidence of a systemic delivery delay problem was found.

## Strategic Insight

The results suggest that delivery estimates may be intentionally conservative.

This strategy can create an "underpromise and overdeliver" effect:

## Potential Benefits

- Increased customer satisfaction
- Reduced SLA violations
- Stronger customer trust
- Positive delivery experience

## Potential Risks

- Customers may perceive delivery times as longer than competitors.
- Some purchase decisions could be negatively affected if estimated delivery windows appear excessively conservative.

Further business analysis would be required to evaluate the trade-off between customer satisfaction and conversion rates.

# Conclusion

The logistics operation demonstrates strong delivery performance and high compliance with promised delivery deadlines.

The analysis found no evidence of widespread delivery delays. Instead, the results indicate a highly reliable fulfillment process with a large proportion of orders arriving earlier than expected.

Future studies could investigate whether delivery estimates are overly conservative and evaluate the impact of delivery promises on customer purchasing behavior.




