import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("="*80)
print("Loading Data...")
print("="*80)

df = pd.read_csv('11_health_risk_classification_1000.csv')
print(f"\nDataset Shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nBasic Statistics:\n{df.describe()}")

# ============================================================================
# 2. IDENTIFY FEATURES AND TARGET
# ============================================================================
print("\n" + "="*80)
print("Identifying Features and Target...")
print("="*80)

# Assume last column is target (modify if needed)
X = df.iloc[:, :-1].copy()
y = df.iloc[:, -1].copy()

print(f"\nTarget Column: {df.columns[-1]}")
print(f"Features: {X.columns.tolist()}")
print(f"Target unique values: {y.unique()}")

# ============================================================================
# 3. ANALYZE SKEWNESS AND PREPROCESS NUMERIC FEATURES
# ============================================================================
print("\n" + "="*80)
print("Analyzing Skewness and Preprocessing Numeric Features...")
print("="*80)

numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
object_features = X.select_dtypes(include=['object']).columns.tolist()

print(f"\nNumeric Features: {numeric_features}")
print(f"Object Features: {object_features}")

# Calculate skewness
skewness_dict = {}
for col in numeric_features:
    skewness = X[col].skew()
    skewness_dict[col] = skewness
    
    # Determine skew direction
    if abs(skewness) < 0.5:
        skew_type = "Normal"
    elif skewness > 0.5:
        skew_type = "Right Skewed"
    elif skewness < -0.5:
        skew_type = "Left Skewed"
    else:
        skew_type = "Approximately Normal"
    
    print(f"{col}: Skewness = {skewness:.4f} ({skew_type})")

# Visualize skewness
fig, axes = plt.subplots(len(numeric_features), 1, figsize=(10, 4*len(numeric_features)))
if len(numeric_features) == 1:
    axes = [axes]

for idx, col in enumerate(numeric_features):
    sns.histplot(data=X, x=col, kde=True, ax=axes[idx])
    axes[idx].set_title(f"Distribution of {col} (Skewness: {skewness_dict[col]:.4f})")

plt.tight_layout()
plt.savefig('skewness_distribution.png', dpi=100, bbox_inches='tight')
print("\n✓ Saved: skewness_distribution.png")
plt.close()

# ============================================================================
# 4. PREPROCESS NUMERIC FEATURES
# ============================================================================
print("\n" + "="*80)
print("Preprocessing Numeric Features...")
print("="*80)

X_processed = X.copy()

# Preprocess numeric features
for col in numeric_features:
    if abs(skewness_dict[col]) > 0.5:
        # Skewed - use PowerTransformer + StandardScaler
        print(f"\n{col}: Skewed - Applying PowerTransformer + StandardScaler")
        pt = PowerTransformer(method='yeo-johnson')
        X_processed[col] = pt.fit_transform(X_processed[[col]])
    else:
        # Normal - use StandardScaler only
        print(f"{col}: Normal - Applying StandardScaler")
        
scaler = StandardScaler()
X_processed[numeric_features] = scaler.fit_transform(X_processed[numeric_features])
print("\n✓ All numeric features scaled")

# ============================================================================
# 5. HANDLE OBJECT/CATEGORICAL FEATURES
# ============================================================================
print("\n" + "="*80)
print("Handling Categorical Features...")
print("="*80)

if object_features:
    print(f"Using pd.get_dummies for: {object_features}")
    X_processed = pd.get_dummies(X_processed, columns=object_features, drop_first=True)
    print(f"Shape after one-hot encoding: {X_processed.shape}")
else:
    print("No categorical features found")

print(f"\nFinal Features Shape: {X_processed.shape}")
print(f"Features: {X_processed.columns.tolist()}")

# ============================================================================
# 6. TRAIN-TEST SPLIT
# ============================================================================
print("\n" + "="*80)
print("Train-Test Split (80-20)...")
print("="*80)

X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain set size: {X_train.shape[0]} ({X_train.shape[0]/len(y)*100:.1f}%)")
print(f"Test set size: {X_test.shape[0]} ({X_test.shape[0]/len(y)*100:.1f}%)")

# ============================================================================
# 7. TRAIN MULTIPLE CLASSIFIERS
# ============================================================================
print("\n" + "="*80)
print("Training Multiple Classifiers...")
print("="*80)

classifiers = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'KNN Classifier': KNeighborsClassifier(n_neighbors=5),
    'SGD Classifier': SGDClassifier(max_iter=1000, random_state=42),
    'KNeighbors Classifier': KNeighborsClassifier(n_neighbors=3),
    'SVC': SVC(kernel='rbf', random_state=42),
    'Gaussian NB': GaussianNB(),
    'Multinomial NB': MultinomialNB()
}

results = {}

for clf_name, clf in classifiers.items():
    print(f"\n{'─'*60}")
    print(f"Training: {clf_name}")
    print(f"{'─'*60}")
    
    try:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        results[clf_name] = {
            'model': clf,
            'accuracy': accuracy,
            'predictions': y_pred,
            'y_true': y_test
        }
        
        print(f"Accuracy Score: {accuracy:.4f}")
        print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    except Exception as e:
        print(f"⚠ Error training {clf_name}: {str(e)}")
        print(f"  Note: {clf_name} requires non-negative features (count data)")
        results[clf_name] = {
            'model': None,
            'accuracy': 0.0,
            'predictions': None,
            'y_true': y_test,
            'error': str(e)
        }

# ============================================================================
# 8. COMPARE RESULTS - ACCURACY TABLE
# ============================================================================
print("\n" + "="*80)
print("MODEL COMPARISON - ACCURACY SCORES")
print("="*80)

# Create results dataframe (filter out failed models)
results_df = pd.DataFrame([
    {'Model': model_name, 'Accuracy': metrics['accuracy']}
    for model_name, metrics in results.items()
    if 'error' not in metrics
]).sort_values('Accuracy', ascending=False).reset_index(drop=True)

print("\n")
print(results_df.to_string(index=False))

# Find best model
best_model_name = results_df.iloc[0]['Model']
best_accuracy = results_df.iloc[0]['Accuracy']

print("\n" + "="*80)
print(f"🏆 BEST MODEL: {best_model_name}")
print(f"   Accuracy: {best_accuracy:.4f}")
print("="*80)

# Save results table
results_df.to_csv('model_comparison_results.csv', index=False)
print("\n✓ Saved: model_comparison_results.csv")

# ============================================================================
# 9. DETAILED REPORT FOR BEST MODEL
# ============================================================================
print("\n" + "="*80)
print(f"DETAILED REPORT - {best_model_name}")
print("="*80)

best_model = results[best_model_name]['model']
y_pred_best = results[best_model_name]['predictions']

print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred_best)}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred_best)}")

# ============================================================================
# 10. PREDICTION FUNCTION
# ============================================================================
print("\n" + "="*80)
print("Creating Prediction Function...")
print("="*80)

def predict_health_risk(input_data_dict):
    """
    Predict health risk using the best model.
    
    Parameters:
    -----------
    input_data_dict : dict
        Dictionary with feature names as keys and values
        
    Returns:
    --------
    prediction : str or int
        The predicted health risk category
    probability : float
        Confidence score (if available)
    """
    # Create DataFrame from input
    input_df = pd.DataFrame([input_data_dict])
    
    # Apply same preprocessing as training data
    input_processed = input_df.copy()
    
    # Preprocess numeric features
    for col in numeric_features:
        if col in input_processed.columns:
            if abs(skewness_dict[col]) > 0.5:
                pt = PowerTransformer(method='yeo-johnson')
                input_processed[col] = pt.fit_transform(input_processed[[col]])
    
    # Scale
    input_processed[numeric_features] = scaler.transform(input_processed[numeric_features])
    
    # Handle categorical features
    if object_features:
        input_processed = pd.get_dummies(input_processed, columns=object_features, drop_first=True)
    
    # Ensure same features as training
    for col in X_processed.columns:
        if col not in input_processed.columns:
            input_processed[col] = 0
    
    input_processed = input_processed[X_processed.columns]
    
    # Make prediction
    prediction = best_model.predict(input_processed)[0]
    
    # Get probability if available
    if hasattr(best_model, 'predict_proba'):
        probabilities = best_model.predict_proba(input_processed)[0]
        max_prob = max(probabilities)
    else:
        max_prob = None
    
    return {
        'prediction': prediction,
        'probability': max_prob,
        'model_used': best_model_name
    }

print("✓ Prediction function created successfully")

# ============================================================================
# 11. EXAMPLE PREDICTIONS
# ============================================================================
print("\n" + "="*80)
print("EXAMPLE PREDICTIONS")
print("="*80)

# Create sample input from first test sample
sample_input = X_test.iloc[0].to_dict()
print(f"\nSample Input (from test data):")
for key, value in list(sample_input.items())[:5]:
    print(f"  {key}: {value}")
print("  ...")

prediction_result = predict_health_risk(sample_input)
print(f"\nPrediction Result:")
print(f"  Predicted Health Risk: {prediction_result['prediction']}")
if prediction_result['probability']:
    print(f"  Confidence: {prediction_result['probability']:.4f}")
else:
    print(f"  Confidence: N/A")
print(f"  Model Used: {prediction_result['model_used']}")

# ============================================================================
# 12. SAVE MODEL AND PREPROCESSING INFO
# ============================================================================
print("\n" + "="*80)
print("Saving Model and Configuration...")
print("="*80)

import pickle

# Save model
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
print("✓ Saved: best_model.pkl")

# Save preprocessing info
preprocessing_info = {
    'skewness_dict': skewness_dict,
    'numeric_features': numeric_features,
    'object_features': object_features,
    'scaler': scaler,
    'best_model_name': best_model_name,
    'best_accuracy': best_accuracy
}

with open('preprocessing_info.pkl', 'wb') as f:
    pickle.dump(preprocessing_info, f)
print("✓ Saved: preprocessing_info.pkl")

# Save feature names
feature_names = X_processed.columns.tolist()
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(feature_names, f)
print("✓ Saved: feature_names.pkl")

# ============================================================================
# 13. SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)

summary = f"""
Dataset: 11_health_risk_classification_1000.csv
Total Samples: {len(df)}
Total Features: {len(X.columns)}

Numeric Features: {len(numeric_features)}
Categorical Features: {len(object_features)}

Train Set Size: {X_train.shape[0]} (80%)
Test Set Size: {X_test.shape[0]} (20%)

Models Tested: {len(classifiers)}
Best Model: {best_model_name}
Best Accuracy: {best_accuracy:.4f}

Output Files Generated:
1. skewness_distribution.png - Distribution plots of all numeric features
2. model_comparison_results.csv - Accuracy comparison table
3. best_model.pkl - Trained best model (serialized)
4. preprocessing_info.pkl - Preprocessing configuration
5. feature_names.pkl - Feature names used in training
"""

print(summary)

# Save summary
with open('SUMMARY_REPORT.txt', 'w') as f:
    f.write(summary)
print("✓ Saved: SUMMARY_REPORT.txt")

print("\n✓ Pipeline completed successfully!")
print("="*80)
