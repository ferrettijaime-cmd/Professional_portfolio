import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

load_dotenv("/opt/airflow/ml_forecasting_db.env")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = None

try:
    engine = create_engine(url)
    X_train_query="""
                select *
                from 
                    features_training.x_train_dataset
    """
    X_test_query="""
                select *
                from 
                    features_training.x_test_dataset
    """
    y_train_query="""
                 select *
                 from 
                     features_training.y_train_dataset
    """
    y_test_query="""
                select *
                from 
                    features_training.y_test_dataset
    """
    print("The data extraction was successful!!!")

    X_train = pd.read_sql(X_train_query, con=engine)
    X_train["order_day"] = pd.to_datetime(X_train["order_day"])
    X_train.set_index('order_day', inplace=True)

    X_test = pd.read_sql(X_test_query, con=engine)
    X_test["order_day"] = pd.to_datetime(X_test["order_day"])
    X_test.set_index('order_day', inplace=True)

    y_train = pd.read_sql(y_train_query, con=engine).squeeze()

    y_test = pd.read_sql(y_test_query, con=engine).squeeze()

    print("Data separation successfully completed!!!")

except Exception as e:
    print("During data extraction")
    import traceback
    traceback.print_exc()
    raise

try:
    from sklearn.linear_model import LinearRegression

    lr_model = LinearRegression()

    lr_model.fit(X_train, y_train)

    from sklearn.ensemble import RandomForestRegressor

    rf_model = RandomForestRegressor( n_estimators=100, random_state=42)

    rf_model.fit(X_train, y_train)

    from xgboost import XGBRegressor

    xgb_model = XGBRegressor(n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42)

    xgb_model.fit(X_train, y_train)

    lr_predict = lr_model.predict(X_test)

    rf_predict = rf_model.predict(X_test)

    xgb_predict = xgb_model.predict(X_test)
    print("Training and predictions successfully completed!!!")

except Exception as e:
    print("During training")
    import traceback
    traceback.print_exc()
    raise

try:
    from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error)
    import numpy as np

    def evaluate_model(y_true, x_predict):
        mae = mean_absolute_error(y_true, x_predict)
        mse = mean_squared_error(y_true, x_predict)
        mape = mean_absolute_percentage_error(y_true, x_predict)
        return mae, mse, mape
    
    mae_lr, mse_lr, mape_lr = evaluate_model(y_test, lr_predict) 

    mae_rf, mse_rf, mape_rf = evaluate_model(y_test, rf_predict)

    mae_xgb, mse_xgb, mape_xgb = evaluate_model(y_test, xgb_predict)

    metric_results = pd.DataFrame({"MODELS": ["Linear Regression", "Random Forest", "XGBoost"], 
                        "MAE": [mae_lr, mae_rf, mae_xgb], 
                        "MSE": [mse_lr, mse_rf, mse_xgb], 
                        "MAPE": [mape_lr, mape_rf, mape_xgb]})
    
    predicted_values = y_test.to_frame(name="Real_result")
    predicted_values[["LR_values", "RF_values", "XGB_values"]] = list(zip(lr_predict, rf_predict,xgb_predict))

    print("Df of metrics results and predicted values ​​created with successes!!!")

except Exception as e:
    print("During the metrics result")
    import traceback
    traceback.print_exc()
    raise

try:
    metric_results.to_sql(
        name="metrics_results",
        con=engine,
        schema="metrics",
        if_exists="replace",
        index=False
    )

    predicted_values.to_sql(
        name="predicted_values",
        con=engine,
        schema="predictions",
        if_exists="replace",
        index=False      
    )

except Exception as e:
    print("During the data transmission phase to Postgres")
    import traceback
    traceback.print_exc()
    raise
   
finally:
    if engine:
        engine.dispose()

