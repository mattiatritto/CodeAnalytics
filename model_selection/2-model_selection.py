import os
import pandas as pd
import numpy as np
import sys
import joblib
from scipy.io import arff

from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.utils import shuffle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import RobustScaler



f =  open('training.log', 'w')
sys.stdout = f



for random_state in range (0, 1):

    print(f"[0]: Testing Random State [{random_state}]...")



    # Parameters that can be modified
    dataset_file_path = os.path.abspath("datasets/1-china-augmented.csv")
    features = ["AFP", "Input", "Output", "Enquiry", "File", "Interface", "Effort"]
    target_variable = "Duration"
    test_size = 0.1
    k_folds = 5
    scoring = 'r2'
    models_params = {
        "Linear Regression with L2 regularization": {
            "name": Ridge(),
            "params": {"alpha": [10, 100.0]},
        },
        "Support Vector Machine": {
            "name": SVR(),
            "params": {
                "C": [0.01, 0.1],
                "epsilon": [0.1, 0.5],
                "kernel": ["rbf"],
            },
        },
        "Random Forest": {
            "name": RandomForestRegressor(random_state=random_state),
            "params": {
                "n_estimators": [110, 120, 130],
                "max_depth": [10, 20],
                "min_samples_split": [2, 5],
                "min_samples_leaf": [1, 2, 5],
            },
        },
        "Neural Network": {
            "name": MLPRegressor(max_iter=15000, random_state=random_state),
            "params": {
                "hidden_layer_sizes": [(64, 32, 16), (64, 32, 16, 8),
                                       (32, 64, 32), (64, 128, 64),
                                       (64, 32, 64), (64, 32, 16, 32, 64)],
                "activation": ["tanh", "relu"],
                "solver": ["adam"],
                "alpha": [0.0001, 0.01],
                "learning_rate_init": [0.01, 0.1],
            },
        }
    }



    # print(f"[1]: Loading the augmented dataset...")
    dataset = pd.read_csv(dataset_file_path)



    # print(f"[2]: Removing outliers with IQR method...")
    q1 = dataset[target_variable].quantile(0.25)
    q3 = dataset[target_variable].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    dataset = dataset[(dataset[target_variable] >= lower_bound) & (dataset[target_variable] <= upper_bound)]



    # print(f"[3]: Selecting the features and the target variable...")
    X = dataset[features]
    y = dataset[target_variable]



    # print(f"[4]: Shuffling rows...")
    X, y = shuffle(X, y, random_state=random_state)



    # print(f"[5]: Splitting dataset into training and testing...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)




    # mean = X_train.mean(axis=0)
    # std = X_train.std(axis=0)
    # print(f"[6]: Normalize data with Z-score normalization (mean = {mean}, std = {std})")
    # X_train_scaled = (X_train - mean) / std
    # X_test_scaled = (X_test - mean) / std
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)



    # print(f"[7]: Searching for the best model with a Grid Search...")
    results = {}
    r2_scores_grid = {}

    for model_name, model_info in models_params.items():

        grid_search = GridSearchCV(model_info["name"], model_info["params"], cv=k_folds, scoring=scoring)
        grid_search.fit(X_train_scaled, y_train)

        best_model = grid_search.best_estimator_

        y_pred = best_model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        results[model_name] = {
            "best_params": grid_search.best_params_,
            "test_mse": mse,
            "test_rmse": rmse,
            "test_r2_score": r2,
        }

        """
        # Storing both R^2 scores and parameter combinations for all parameter sets tested
        r2_scores_grid[model_name] = {
            'params': grid_search.cv_results_['params'],
            'mean_test_r2_score': grid_search.cv_results_['mean_test_score']
        }
        """

        print(f"[{model_name}]:")
        print(f"  Best Parameters: {results[model_name]['best_params']}")
        print(f"  Test MSE: {results[model_name]['test_mse']:.2f}")
        print(f"  Test RMSE: {results[model_name]['test_rmse']:.2f}")
        print(f"  Test R^2 Score: {results[model_name]['test_r2_score']:.2f}")


    """
    # Showing R^2 scores and corresponding parameter combinations for each model's grid search
    for model_name, grid_data in r2_scores_grid.items():
        print(f"\nR^2 scores and corresponding parameters for {model_name}:")
        for params, r2_score_ in zip(grid_data['params'], grid_data['mean_test_r2_score']):
            print(f"Parameters: {params} => R^2 Score: {r2_score_:.4f}")
    """

    """
    # Retrieve the best parameters from the best model
    best_params = results["Random Forest"]["best_params"]
    final_model = RandomForestRegressor(**best_params, random_state=random_state)
    final_model.fit(X_train_scaled, y_train)
    joblib.dump(final_model, "trained-model.pkl")
    """