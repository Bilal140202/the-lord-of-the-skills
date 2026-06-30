# Data Science / ML Project

## Overview
This is a data science and machine learning project for predictive modeling, data analysis, or ML system development.

## Tech Stack
- **Language**: Python 3.11+
- **Core Libraries**: NumPy, Pandas, Scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **ML Framework**: (Scikit-learn / PyTorch / TensorFlow / XGBoost)
- **Experiment Tracking**: (MLflow / Weights & Biases / TensorBoard)
- **Deployment**: (FastAPI / Flask / Streamlit)

## Project Structure
```
project/
  ├── data/
  │   ├── raw/           # Original, immutable data
  │   └── processed/     # Cleaned, transformed data
  ├── notebooks/         # Jupyter notebooks for exploration
  │   ├── 01_eda.ipynb
  │   ├── 02_modeling.ipynb
  │   └── 03_evaluation.ipynb
  ├── src/               # Production code
  │   ├── data/          # Data loading and preprocessing
  │   ├── features/      # Feature engineering
  │   ├── models/        # Model training and evaluation
  │   └── utils/         # Utility functions
  ├── models/            # Saved model artifacts
  ├── reports/           # Generated reports and figures
  └── tests/             # Unit tests
```

## Key Commands
```bash
jupyter lab                    # Start Jupyter
python src/train.py            # Train model
python src/predict.py          # Make predictions
mlflow ui                      # View experiments
pytest tests/                  # Run tests
```

## Development Workflow

### 1. Data Exploration (Notebook)
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/raw/dataset.csv')

# Overview
print(df.info())
print(df.describe())
print(df.head())

# Check missing values
print(df.isnull().sum())

# Visualize distributions
df.hist(figsize=(12, 10))
plt.tight_layout()

# Check correlations
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

### 2. Data Preprocessing
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Split data FIRST (before any transformations)
X = df.drop('target', axis=1)
y = df['target']

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

# Scale features (fit on train only!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
```

### 3. Model Training
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Start with baseline
from sklearn.dummy import DummyClassifier
baseline = DummyClassifier(strategy='most_frequent')
baseline.fit(X_train_scaled, y_train)
baseline_acc = baseline.score(X_val_scaled, y_val)
print(f'Baseline accuracy: {baseline_acc:.3f}')

# Train actual model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_scaled, y_train)

# Evaluate on validation set
y_pred = model.predict(X_val_scaled)
print(classification_report(y_val, y_pred))
print(confusion_matrix(y_val, y_pred))

# Save model
joblib.dump(model, 'models/rf_model_v1.pkl')
joblib.dump(scaler, 'models/scaler_v1.pkl')
```

### 4. Hyperparameter Tuning
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_scaled, y_train)
print(f'Best params: {grid_search.best_params_}')
print(f'Best CV score: {grid_search.best_score_:.3f}')

best_model = grid_search.best_estimator_
```

### 5. Final Evaluation (Test Set)
```python
# Only evaluate on test set once!
y_test_pred = best_model.predict(X_test_scaled)

print('Test Set Results:')
print(classification_report(y_test, y_test_pred))

# Visualize confusion matrix
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_predictions(y_test, y_test_pred)
plt.title('Confusion Matrix - Test Set')
plt.savefig('reports/confusion_matrix.png')
```

## Notebook Structure Template

```markdown
# Project Title

## 1. Problem Statement
- What are we trying to predict?
- Why is this important?
- What is success criteria?

## 2. Data Loading
- Load data from data/raw/
- Document data source and collection date
- Check data shape and types

## 3. Exploratory Data Analysis
- Missing values
- Data distributions
- Outliers
- Correlations
- Target variable balance

## 4. Data Preprocessing
- Handle missing values
- Feature engineering
- Encoding categorical variables
- Feature scaling
- Train/val/test split

## 5. Baseline Model
- Simple model (mean, mode, or most_frequent)
- Benchmark performance

## 6. Model Training
- Try multiple models
- Cross-validation
- Hyperparameter tuning

## 7. Model Evaluation
- Validation set performance
- Test set performance (final)
- Confusion matrix / residual plots
- Feature importance

## 8. Conclusions
- Best model and performance
- Insights and recommendations
- Next steps
```

## Reproducibility Checklist
```python
# Set ALL random seeds
import numpy as np
import random
import os

def set_seeds(seed=42):
    np.random.seed(seed)
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

    # For PyTorch
    # import torch
    # torch.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)

    # For TensorFlow
    # import tensorflow as tf
    # tf.random.set_seed(seed)

set_seeds(42)
```

## Environment Setup
```bash
# Create environment
conda create -n ml-project python=3.11
conda activate ml-project

# Install dependencies
pip install -r requirements.txt

# Or with conda
conda env create -f environment.yml
```

## Production Deployment
```python
# src/predict.py
import joblib
import pandas as pd

def load_model():
    model = joblib.load('models/rf_model_v1.pkl')
    scaler = joblib.load('models/scaler_v1.pkl')
    return model, scaler

def predict(data: pd.DataFrame):
    model, scaler = load_model()
    X_scaled = scaler.transform(data)
    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)
    return predictions, probabilities
```

## Common Metrics

### Classification
- Accuracy: Overall correctness
- Precision: Of positive predictions, how many were correct
- Recall: Of actual positives, how many we caught
- F1: Harmonic mean of precision and recall
- ROC-AUC: Area under ROC curve

### Regression
- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- R²: Proportion of variance explained
- MAPE: Mean Absolute Percentage Error

## Key Reminders for AI Assistants
1. **Split data first** — Before any transformations
2. **Set random seeds** — For reproducibility
3. **Baseline model** — Always compare against simple baseline
4. **Never test twice** — Only evaluate on test set once
5. **Handle missing values** — Explicitly, never ignore
6. **Visualize everything** — Distributions, correlations, errors
7. **Document assumptions** — What are we assuming about the data?
8. **Check for leakage** — No future information in features

## Version Control
```bash
# Track code
git add notebooks/ src/ requirements.txt
git commit -m "Add initial EDA and baseline model"

# Track data (with DVC)
dvc add data/raw/dataset.csv
dvc add models/rf_model_v1.pkl
git add data/.gitignore models/.gitignore data/raw/dataset.csv.dvc
git commit -m "Track dataset and model"
```

## Troubleshooting
- **Low accuracy**: Check data quality, try more features, tune hyperparameters
- **Overfitting**: Reduce model complexity, add regularization, get more data
- **Underfitting**: Increase model complexity, add features, reduce regularization
- **Data leakage**: Verify train/test split, check feature creation logic
