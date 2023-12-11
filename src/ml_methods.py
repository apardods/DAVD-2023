import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.utils import check_array
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

def fit_linear_regression(y, X):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    lr = LinearRegression().fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    coefficients_df = pd.DataFrame({
        'Var/Metric': ['Intercept'] + list(X.columns),
        'Coef/Value': [lr.intercept_[0]] + list(lr.coef_[0])
    })

    metrics_df = pd.DataFrame({
        'Var/Metric': ['R-squared', 'RMSE', 'MAPE'],
        'Coef/Value': [r2, rmse, mape]
    })
    return pd.concat([coefficients_df, metrics_df], ignore_index=True)


def fit_random_forest(y, X):
    param_grid = {
        'n_estimators': [100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
    }
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    rf = RandomForestRegressor()
    rf_random = RandomizedSearchCV(estimator=rf, param_distributions=param_grid, n_iter=10, cv=3, random_state=42, n_jobs=-1)
    rf_random.fit(X_train, y_train)
    best_params = rf_random.best_params_
    final_rf_model = RandomForestRegressor(**best_params)
    final_rf_model.fit(X_train, y_train.values.ravel())
    y_pred = final_rf_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred.reshape(len(y_pred), 1)) / y_test)) * 100
    coefficients_df = pd.DataFrame({
        'Var/Metric': list(X.columns),
        'Importance/Value':list(final_rf_model.feature_importances_)
    })
    metrics_df = pd.DataFrame({
        'Var/Metric': ['R-squared', 'RMSE', 'MAPE'],
        'Importance/Value': [r2, rmse, mape]
    })
    return pd.concat([coefficients_df, metrics_df], ignore_index=True)

def fit_svm(y, X):
    param_grid = {
        'C': [0.1, 1],
        'kernel': ['linear'],
        'epsilon': [0.1, 0.2],
    }
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    svm = SVR()
    svm_model = RandomizedSearchCV(estimator=svm, param_distributions=param_grid, n_iter=10, cv=3, random_state=42, n_jobs=-1)
    svm_model.fit(X_train, y_train)
    best_params = svm_model.best_params_
    final_svm_model = SVR(**best_params)
    final_svm_model.fit(X_train, y_train)
    y_pred = final_svm_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred.reshape(len(y_pred), 1)) / y_test)) * 100
    coefficients_df = pd.DataFrame({
        'Var/Metric': ['Intercept'] + list(X.columns),
        'Coef/Value': [final_svm_model.intercept_[0]] + list(final_svm_model.coef_[0])
    })

    metrics_df = pd.DataFrame({
        'Var/Metric': ['R-squared', 'RMSE', 'MAPE'],
        'Coef/Value': [r2, rmse, mape]
    })
    return pd.concat([coefficients_df, metrics_df], ignore_index=True)