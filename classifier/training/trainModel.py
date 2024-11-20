#modules for training
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import gc

#modules for evaluation
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

chunk_size = 10000  # Number of rows to process at a time
target_column = "Fraud"
columns_to_drop = ['Transaction ID', 'Date']  # Columns to drop
model_file = 'model.joblib'
columns_file = 'trained_columns.joblib'

# Load training data
data = pd.read_csv('CreditCardData.csv')

# Initialize the model. Class weight is being set due to imbalance of fraud/not fraud
model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, class_weight={0: 1, 1: 8})

# Variables to store cumulative data for validation
X_val = pd.DataFrame()
y_val = pd.Series(dtype=int)
trained_columns = None

# Training loop
reader = pd.read_csv('CreditCardData.csv', chunksize=chunk_size)
for i, chunk in enumerate(reader):
    print(f"Processing chunk {i + 1}")

    # Drop unnecessary columns
    chunk = chunk.drop(columns=columns_to_drop)

    # Split features and target
    y_chunk = chunk[target_column]
    X_chunk = chunk.drop(columns=[target_column])

    # Preprocess features (e.g., one-hot encoding)
    X_chunk = pd.get_dummies(X_chunk)
    
    # Ensure column alignment
    if trained_columns is None:
        trained_columns = X_chunk.columns
    else:
        X_chunk = X_chunk.reindex(columns=trained_columns, fill_value=0)

    # Split chunk into training and validation subsets
    X_train_chunk, X_val_chunk, y_train_chunk, y_val_chunk = train_test_split(
        X_chunk, y_chunk, test_size=0.2, random_state=42
    )
    
    # Train the model incrementally
    model.fit(X_train_chunk, y_train_chunk)
    
    # Collect validation data for final evaluation
    X_val = pd.concat([X_val, X_val_chunk], ignore_index=True)
    y_val = pd.concat([y_val, y_val_chunk], ignore_index=True)
    
    # Cleanup to free memory
    del X_chunk, y_chunk, X_train_chunk, X_val_chunk, y_train_chunk, y_val_chunk
    gc.collect()

print("Training complete.")

# Predictions on test data
y_pred = model.predict(X_val)

# Print classification metrics
print("Classification Report:")
print(classification_report(y_val, y_pred))

# Print Accuracy
accuracy = accuracy_score(y_val, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Confusion Matrix
cm = confusion_matrix(y_val, y_pred)
print("Confusion Matrix:")
print(cm)

# Save Confusion Matrix Plot
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Not Fraud", "Fraud"], yticklabels=["Not Fraud", "Fraud"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
print("Confusion matrix plot saved as 'confusion_matrix.png'.")

# ROC-AUC Score
roc_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
print(f"ROC-AUC Score: {roc_auc:.2f}")

# Save the trained model and column information
joblib.dump(model, model_file)
joblib.dump(trained_columns, columns_file)
print(f"Model saved to {model_file}")
print(f"Trained columns saved to {columns_file}")

print("Model training complete. Model saved as 'model.joblib'")
