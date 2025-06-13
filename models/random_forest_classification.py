import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import time

# Generate a large synthetic classification dataset
X, y = make_classification(
    n_samples=100000,  # .1 million samples
    n_features=20,      # 20 features
    n_informative=15,   # 15 informative features
    n_redundant=5,      # 5 redundant features
    n_classes=3,        # 3 classes for classification
    random_state=42
)

print("Dataset generated successfully!")
print(f"Shape of X: {X.shape}")
print(f"Shape of y: {y.shape}")

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

# Train the model
start = time.time()
clf.fit(X_train, y_train)
end = time.time()

print(f"\nTraining completed in {end - start:.2f} seconds.")

# Predict on test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

# Detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
