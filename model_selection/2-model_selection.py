import os
import pandas as pd
import numpy as np
import joblib
from scipy.io import arff

from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler



file_path = os.path.abspath('datasets/1-china.arff')
data = arff.loadarff(file_path)
df = pd.DataFrame(data[0])
for column in df.select_dtypes([np.object]):
    df[column] = df[column].str.decode('utf-8')



# Remove outliers using the IQR method
Q1 = df['Duration'].quantile(0.25)
Q3 = df['Duration'].quantile(0.75)
IQR = Q3 - Q1



# Filter outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Duration'] >= lower_bound) & (df['Duration'] <= upper_bound)]


# Selecting the features and target variables
X = df[['AFP', 'Effort', 'Input', 'Output', 'Enquiry', 'File', 'Interface']]
y = df['Duration']



# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)



# Scale features using Z-score normalization
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)



# Define the models and their hyperparameter grids
models_params = {
    'Linear Regression with L2 regularization': {
        'model': Ridge(),
        'params': {
            'alpha': [10, 100.0, 1000.0]
        }
    },
    'Support Vector Machine': {
        'model': SVR(),
        'params': {
            'C': [0.01, 0.1, 1.0],
            'epsilon': [0.01, 0.1, 0.5],
            'kernel': ['linear', 'rbf']
        }
    },
    'Neural Network': {
        'model': MLPRegressor(max_iter=1000, random_state=42),
        'params': {
            'hidden_layer_sizes': [(64, 32, 16)],
            'activation': ['relu', 'tanh'],
            'learning_rate_init': [0.001, 0.01]
        }
    },
    'Random Forest': {
        'model': RandomForestRegressor(random_state=41),
        'params': {
            'n_estimators': [90, 95, 100, 105, 110],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2, 4]
        }
    }
}



# Train and evaluate each model using Grid Search
results = {}

for model_name, model_info in models_params.items():

    grid_search = GridSearchCV(model_info['model'], model_info['params'], cv=5, scoring='r2')
    grid_search.fit(X_train_scaled, y_train)
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    results[model_name] = {
        'best_params': grid_search.best_params_,
        'test_mse': mse,
        'test_rmse': rmse,
        'test_r2_score': r2
    }



for model_name, metrics in results.items():
    print(f"{model_name}:")
    print(f"  Best Parameters: {metrics['best_params']}")
    print(f"  Test MSE: {metrics['test_mse']:.2f}")
    print(f"  Test RMSE: {metrics['test_rmse']:.2f}")
    print(f"  Test R^2 Score: {metrics['test_r2_score']:.2f}")



# Retrieve the best parameters from the results
best_params = results['Random Forest']['best_params']
final_model = RandomForestRegressor(**best_params, random_state=41)
final_model.fit(X_train_scaled, y_train)
joblib.dump(final_model, 'best_random_forest_model.pkl')