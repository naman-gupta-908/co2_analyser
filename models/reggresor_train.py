import numpy as np
import pandas as pd
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import time

# Generate synthetic regression dataset
X, y = make_regression(
    n_samples=100000,   # 100K samples
    n_features=20,      # 20 features
    n_informative=15,   # 15 informative features
    noise=0.1,          # small noise
    random_state=42
)

print("Dataset generated successfully!")
print(f"Shape of X: {X.shape}")
print(f"Shape of y: {y.shape}")

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize regressor
regressor = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

# Train the model
start = time.time()
regressor.fit(X_train, y_train)
end = time.time()

print(f"\nTraining completed in {end - start:.2f} seconds.")

# Predict on test set
y_pred = regressor.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"\nMean Squared Error: {mse:.4f}")
print(f"Root Mean Squared Error: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")
