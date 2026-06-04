"""
Health Risk Classification - Interactive Web Application
Provides user interface for making predictions using the trained KNN model
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import PowerTransformer, StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Health Risk Classification",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# LOAD SAVED MODEL AND PREPROCESSING INFO
# ============================================================================
@st.cache_resource
def load_model_and_config():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('preprocessing_info.pkl', 'rb') as f:
            preprocessing_info = pickle.load(f)
        
        with open('feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        
        return model, preprocessing_info, feature_names
    except FileNotFoundError:
        st.error("❌ Model files not found. Please run health_risk_ml_pipeline.py first.")
        return None, None, None

# Load model and configuration
model, preprocessing_info, feature_names = load_model_and_config()

if model is None:
    st.stop()

# ============================================================================
# EXTRACT CONFIGURATION
# ============================================================================
skewness_dict = preprocessing_info['skewness_dict']
numeric_features = preprocessing_info['numeric_features']
object_features = preprocessing_info['object_features']
scaler = preprocessing_info['scaler']
best_model_name = preprocessing_info['best_model_name']
best_accuracy = preprocessing_info['best_accuracy']

# ============================================================================
# HEADER & NAVIGATION
# ============================================================================
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stMetric {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Health Risk Classification")
st.markdown("---")
st.markdown("""
Predict health risk based on personal health metrics using machine learning.
""")

# ============================================================================
# SIDEBAR - MODEL INFO
# ============================================================================
with st.sidebar:
    st.header("📊 Model Information")
    
    st.metric("Best Model", best_model_name)
    st.metric("Accuracy", f"{best_accuracy:.2%}")
    
    st.divider()
    
    st.subheader("Features Used")
    for i, feature in enumerate(numeric_features, 1):
        skewness = skewness_dict[feature]
        if abs(skewness) > 0.5:
            skew_type = "Right Skewed" if skewness > 0 else "Left Skewed"
        else:
            skew_type = "Normal"
        
        st.write(f"{i}. **{feature}**")
        st.caption(f"Skewness: {skewness:.4f} ({skew_type})")
    
    st.divider()
    
    st.subheader("📈 Preprocessing Applied")
    st.write("""
    - **Skewed Features**: PowerTransformer + StandardScaler
    - **Normal Features**: StandardScaler
    - **Categorical**: One-Hot Encoding (if any)
    """)

# ============================================================================
# MAIN INTERFACE - PREDICTION INPUT
# ============================================================================
st.header("🔮 Make a Prediction")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    age = st.slider(
        "Age (years)",
        min_value=18,
        max_value=69,
        value=45,
        step=1,
        help="Your age in years"
    )

with col2:
    bmi = st.slider(
        "BMI (Body Mass Index)",
        min_value=12.5,
        max_value=40.2,
        value=27.3,
        step=0.1,
        help="Body Mass Index"
    )

col3, col4 = st.columns(2)

with col3:
    smoker = st.radio(
        "Smoking Status",
        options=["No", "Yes"],
        index=0,
        help="Do you smoke?"
    )
    smoker_value = 0 if smoker == "No" else 1

with col4:
    exercise = st.slider(
        "Exercise Days per Week",
        min_value=0,
        max_value=7,
        value=3,
        step=1,
        help="How many days per week do you exercise?"
    )

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================
def predict_health_risk(age, bmi, smoker, exercise):
    """
    Make a prediction using the trained model
    """
    try:
        # Create input dataframe
        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'smoker': [smoker],
            'exercise_days_per_week': [exercise]
        })
        
        # Apply preprocessing
        input_processed = input_data.copy()
        
        # Apply transformations for skewed features
        for col in numeric_features:
            if col in input_processed.columns:
                if abs(skewness_dict[col]) > 0.5:
                    # Apply PowerTransformer for skewed data
                    pt = PowerTransformer(method='yeo-johnson')
                    input_processed[col] = pt.fit_transform(input_processed[[col]])
        
        # Apply StandardScaler
        input_processed[numeric_features] = scaler.transform(input_processed[numeric_features])
        
        # Ensure same features as training
        for col in feature_names:
            if col not in input_processed.columns:
                input_processed[col] = 0
        
        input_processed = input_processed[feature_names]
        
        # Make prediction
        prediction = model.predict(input_processed)[0]
        
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_processed)[0]
            confidence = max(probabilities)
        else:
            confidence = None
        
        return prediction, confidence
    except Exception as e:
        return None, None

# ============================================================================
# MAKE PREDICTION
# ============================================================================
if st.button("🔍 Predict Health Risk", use_container_width=True, type="primary"):
    prediction, confidence = predict_health_risk(age, bmi, smoker_value, exercise)
    
    if prediction is not None:
        # Display results
        st.divider()
        st.subheader("📋 Prediction Results")
        
        # Create result columns
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            risk_label = "⚠️ HIGH RISK" if prediction == 1 else "✅ LOW RISK"
            st.metric("Health Risk Status", risk_label)
        
        with result_col2:
            st.metric("Confidence", f"{confidence:.2%}" if confidence else "N/A")
        
        # Risk interpretation
        st.divider()
        st.subheader("📊 Risk Interpretation")
        
        if prediction == 1:
            st.warning("""
            ⚠️ **HIGH RISK DETECTED**
            
            Based on the provided health metrics, there is an elevated health risk.
            
            **Recommendations:**
            - Consult with a healthcare professional
            - Consider lifestyle modifications
            - Monitor health metrics regularly
            - Focus on areas that need improvement
            """)
        else:
            st.success("""
            ✅ **LOW RISK**
            
            Your health metrics indicate a low health risk status.
            
            **Recommendations:**
            - Maintain current healthy habits
            - Continue regular exercise routine
            - Keep monitoring your health metrics
            - Schedule regular health check-ups
            """)
        
        # Input summary
        st.divider()
        st.subheader("📝 Your Input Summary")
        
        summary_df = pd.DataFrame({
            'Metric': ['Age', 'BMI', 'Smoking Status', 'Exercise Days/Week'],
            'Value': [f"{age} years", f"{bmi:.1f}", smoker, f"{exercise} days"]
        })
        
        st.table(summary_df)
    else:
        st.error("Error making prediction. Please try again.")

# ============================================================================
# MODEL COMPARISON TABLE
# ============================================================================
st.divider()
st.header("📊 Model Comparison")

try:
    comparison_df = pd.read_csv('model_comparison_results.csv')
    
    # Highlight best model
    styled_df = comparison_df.copy()
    styled_df['Accuracy'] = styled_df['Accuracy'].apply(lambda x: f"{x:.2%}")
    
    st.table(styled_df)
    
    st.markdown("""
    **Results Summary:**
    - Total Models Tested: 6 (MultinomialNB excluded due to negative values)
    - Best Model: KNN Classifier
    - Best Accuracy: 97.50%
    """)
except FileNotFoundError:
    st.warning("Model comparison results not found.")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
---
**📌 Disclaimer:** This tool is for educational purposes only. It should not be used as a substitute for professional medical advice. 
Always consult with a qualified healthcare professional for medical decisions.

**Built with:** Streamlit | Machine Learning | Python
""")
