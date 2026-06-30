# GitHub Copilot Instructions — Data Science / ML

## Project Context
This is a data science and machine learning project for predictive modeling and data analysis with Python.

## Code Generation Rules

### Data Exploration
```python
import pandas as pd
import seaborn as sns

# Always start with overview
df.info()
df.describe()
df.head()

# Check missing values
df.isnull().sum()

# Visualize distributions
df.hist(figsize=(12, 10))

# Check correlations
sns.heatmap(df.corr(), annot=True)
```

### Train/Test Split
```python
from sklearn.model_selection import train_test_split
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Split BEFORE any transformations
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # For classification
)
```

### Feature Scaling
```python
from sklearn.preprocessing import StandardScaler

# Fit on train, transform both
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Never fit on test!
```

### Model Training with Baseline
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier

# Always start with baseline
baseline = DummyClassifier(strategy='most_frequent')
baseline.fit(X_train, y_train)
print(f'Baseline: {baseline.score(X_test, y_test):.3f}')

# Train actual model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
print(f'Model: {model.score(X_test, y_test):.3f}')
```

### Model Evaluation
```python
from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(X_test)

# Classification
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Regression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)
```

### Reproducibility
```python
# Set all random seeds
import numpy as np
import random

def set_seeds(seed=42):
    np.random.seed(seed)
    random.seed(seed)

set_seeds(42)
```

### Save Model
```python
import joblib

# Save model and preprocessing
joblib.dump(model, 'models/model_v1.pkl')
joblib.dump(scaler, 'models/scaler_v1.pkl')

# Load model
model = joblib.load('models/model_v1.pkl')
```

## Common Mistakes to Avoid
- ❌ Don't train on test data
- ❌ Don't fit scaler/encoder on test data
- ❌ Don't skip baseline model
- ❌ Don't forget random seeds
- ❌ Don't use accuracy for imbalanced data
- ❌ Don't evaluate on test set multiple times

## When Generating Code
1. Set random seeds for reproducibility
2. Split data before transformations
3. Fit preprocessing only on training data
4. Start with baseline model
5. Use appropriate metrics
6. Visualize results (confusion matrix, residuals)
7. Handle missing values explicitly
8. Document data sources and assumptions
