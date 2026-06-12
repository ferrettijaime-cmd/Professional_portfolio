# Revenue Forecasting: Statistical Models vs Machine Learning

## Project Overview

This project aims to forecast future e-commerce revenue using both statistical forecasting methods and machine learning models. Several approaches were tested, including Moving Average, Holt Linear Trend, SARIMA, Linear Regression, Random Forest, and XGBoost, in order to compare their predictive performance on the Olist e-commerce dataset

Due to the limited size of the dataset, feature engineering techniques such as lag variables and rolling averages were implemented to improve model learning and forecasting capability.
The main objective of the project is to evaluate which modeling approach performs best for short-term revenue prediction.

## The tools used for this analysis are detailed below.

![Tools_detail](Images\tools_detail.png)

# Statistical Forecasting Methods

## EDA & Visualization

The line graph shows that most weekly peaks range between 100,000 and 300,000, with an extreme peak of approximately 400,000 in late 2017. The fact that the mean ($22,000) and median ($20,000) are so similar demonstrates that, on a daily basis, the behavior is highly symmetrical and the bias is controlled.

![Sales_trend](Images\sales_trend.png)

Daily Consistency vs. Weekly Volume: The business maintains a highly stable and symmetrical daily operation, with an average daily revenue of $22,064 and controlled volatility ($\sigma = $12,594).Weekly Grouping Effect: By consolidating sales by week, the true potential of the business is revealed. The bimodal distribution of the histogram shows that, in weeks of regular operation, the company consistently generates between $100,000 and $250,000 in revenue per week.

![Sales_distribution](Images\sales_distribution.png)

## Final Result

Winning Model (Traditional): Holt's method shows the best fit among the statistical options evaluated (MAE: ~44.943; MAPE: 4599%), slightly outperforming strict exponential smoothing and SARIMA.

Metrics Diagnosis: Despite being the best statistical option, the absolute errors are critically high (the models fail to predict almost half of the actual value). SARIMA's poor performance (MAPE: 5157%) confirms that the series structure has complex dynamics that are difficult to model linearly.

Critical Next Step: Given the inefficiency of traditional techniques in absorbing volatility, it was decided to shift development toward Machine Learning approaches to model nonlinear relationships and reduce the error to acceptable operating thresholds.

# Machine Learning

## Feature Engineering

With the aim of capturing the non-linear patterns, seasonality, and temporal dependencies that traditional statistical models failed to absorb, a set of predictive variables (features) was structured based on the date and historical behavior of revenue.

## Final Result

Machine Learning Model ResultsAfter incorporating feature engineering (calendar features, lags, and moving windows), prediction performance improved dramatically.

Surprisingly, the Linear Regression model achieved the best overall performance, reaching a critically low margin of error (MAPE: 56% and MAE: 5,560.28), outperforming complex algorithms such as Random Forest and XGBoost.This performance indicates that feature engineering successfully linearized the temporal relationships of the dataset. 

By constructing robust predictive variables (such as lags and 7- and 14-day moving averages), the original high volatility problem was simplified, allowing a simpler, more direct model to capture the trend more accurately and without the risk of overfitting that decision tree-based models often exhibit with stable time series.

![Real_vs_Linear_R](Images\real_vs_linear_regr.png)

Visual Evaluation: Actual Values ​​vs. Prediction (Linear Regression)The comparative graph demonstrates that the Linear Regression model accurately captures the overall trend and macro cycles of daily revenue. Thanks to the moving average and lag variables (7- and 14-day features), the red line (prediction) acts as intelligent smoothing, faithfully tracking the ups and downs of the business throughout the months (May - September 2018).

However, the visual gap between the two lines explains the origin of the MAPE (56%): the model is unable to replicate the extreme peaks and valleys of daily activity (the "noise" or pure volatility). This is because linear regression seeks to minimize overall error, sacrificing daily outliers to offer a more conservative and reliable forecast, avoiding overfitting.

# Conclusion

This project compared traditional statistical forecasting methods with modern machine learning approaches to predict short-term e-commerce revenue using the Olist dataset.

Among the statistical models, Holt Linear Trend achieved the best overall performance, outperforming Moving Average, Exponential Smoothing, and SARIMA. This suggests that the dataset contains a clear trend component, while more complex statistical models such as SARIMA struggled due to the limited size and volatility of the data.

In the machine learning stage, feature engineering techniques such as lag variables and rolling averages significantly improved predictive performance. Linear Regression achieved the lowest forecasting error among all ML models tested, slightly outperforming Random Forest and XGBoost. The strong linear relationships observed during exploratory analysis explain why a simpler regression-based approach adapted well to the dataset.

Overall, the results demonstrate that feature engineering played a critical role in improving forecasting accuracy. Additionally, the project highlights that more complex models do not always guarantee better performance, especially when working with limited historical data.
