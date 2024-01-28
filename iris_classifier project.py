# -*- coding: utf-8 -*-
"""Iris classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1evN6NOfmh7LJMbzmgG4tTxETIjNLKj8y
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV


# Step 1: Data Exploration
# Load the dataset
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
data = pd.read_csv('/content/sample_data/iris_data.txt', delimiter=',', names=column_names)  # Specify column names

# Display basic dataset information
print("\nDataset Information:\n")
print(data.info())

# Display the first few rows of the dataset
print("\n\nFirst Few Rows of the Dataset:")
print(data.head())

# Step 2: Data Preprocessing
# Handle missing values (if any)
data.dropna(inplace=True)

# Encode the categorical target variable (species)
label_encoder = LabelEncoder()
data['species'] = label_encoder.fit_transform(data['species'])

# Split the dataset into a training set and a testing set
X = data.drop('species', axis=1)
y = data['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model Selection
# Choose a simple machine learning algorithm (Logistic Regression)
model = LogisticRegression()

# Step 4: Model Training
model.fit(X_train, y_train)

# Step 5: Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

print("\n\nModel Evaluation:")
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

# Step 6: Prediction
print("\n\nEnter flower measurements for prediction:")
sepal_length = float(input("Sepal Length: "))
sepal_width = float(input("Sepal Width: "))
petal_length = float(input("Petal Length: "))
petal_width = float(input("Petal Width: "))
new_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
predicted_species = model.predict(new_data)

predicted_species_label = label_encoder.inverse_transform(predicted_species)

print()
# Step 7: Visualization

# Scatter plot for sepal length vs sepal width
plt.figure(figsize=(10, 6))
for species in data['species'].unique():
    species_data = data[data['species'] == species]
    plt.scatter(species_data['sepal_length'], species_data['sepal_width'], label=species)

plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.title('Scatter Plot: Sepal Length vs Sepal Width')
plt.legend()
plt.show()
print()
# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.get_cmap('Blues'))
plt.title('Confusion Matrix')
plt.colorbar()
print()
tick_marks = np.arange(len(label_encoder.classes_))
plt.xticks(tick_marks, label_encoder.classes_, rotation=45)
plt.yticks(tick_marks, label_encoder.classes_)
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()
print()
# Step 8: Model Tuning
#hyperparameter tuning using GridSearchCV
param_grid = {
    'C': [0.01, 0.1, 1.0, 10.0],
    'solver': ['lbfgs', 'liblinear'],
    'max_iter': [100, 200, 300]
}

grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
best_model = grid_search.best_estimator_
print("\n\nModel Tuning:")
print("Best Hyperparameters:", best_params)

# Re-train the model with the best hyperparameters
best_model.fit(X_train, y_train)

# Evaluate the best model
y_pred_best = best_model.predict(X_test)
accuracy_best = accuracy_score(y_test, y_pred_best)
report_best = classification_report(y_test, y_pred_best, target_names=label_encoder.classes_)

print("\n\nModel Evaluation with Best Model:")
print(f"Accuracy with Best Model: {accuracy_best}")
print("Classification Report with Best Model:")
print(report_best)
print()
print(f"\n\nPredicted Flower Species: {predicted_species_label[0]}\n\n")