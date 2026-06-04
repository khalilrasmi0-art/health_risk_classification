"""
Health Risk Classification - Command Line Prediction Interface
Simple input/output for quick predictions
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer, StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LOAD MODEL AND CONFIGURATION
# ============================================================================
print("\n" + "="*70)
print("🏥 HEALTH RISK CLASSIFICATION - PREDICTION INTERFACE")
print("="*70)

try:
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('preprocessing_info.pkl', 'rb') as f:
        preprocessing_info = pickle.load(f)
    
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    print("✅ Model loaded successfully")
except FileNotFoundError:
    print("❌ Error: Model files not found!")
    print("   Please run: python health_risk_ml_pipeline.py")
    exit()

# Extract configuration
skewness_dict = preprocessing_info['skewness_dict']
numeric_features = preprocessing_info['numeric_features']
scaler = preprocessing_info['scaler']
best_model_name = preprocessing_info['best_model_name']
best_accuracy = preprocessing_info['best_accuracy']

print(f"✅ Using Model: {best_model_name}")
print(f"✅ Model Accuracy: {best_accuracy:.2%}")

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================
def predict_health_risk(age, bmi, smoker, exercise):
    """Make prediction with given inputs"""
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
        
        # Get probability
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_processed)[0]
            confidence = max(probabilities)
        else:
            confidence = None
        
        return prediction, confidence
    except Exception as e:
        return None, None

# ============================================================================
# INPUT LOOP
# ============================================================================
print("\n" + "="*70)
print("ENTER YOUR HEALTH METRICS (or 'quit' to exit)")
print("="*70)

while True:
    try:
        print("\n" + "-"*70)
        
        # Get inputs
        print("\n📋 Input Your Health Information:")
        
        age = float(input("  Age (18-69 years): "))
        if age < 18 or age > 69:
            print("  ⚠️  Age should be between 18-69")
            continue
        
        bmi = float(input("  BMI (12.5-40.2): "))
        if bmi < 12.5 or bmi > 40.2:
            print("  ⚠️  BMI should be between 12.5-40.2")
            continue
        
        smoker_input = input("  Smoking Status (yes/no): ").lower().strip()
        if smoker_input in ['yes', 'y', '1']:
            smoker = 1
            smoker_str = "Yes"
        elif smoker_input in ['no', 'n', '0']:
            smoker = 0
            smoker_str = "No"
        else:
            print("  ⚠️  Please enter 'yes' or 'no'")
            continue
        
        exercise = float(input("  Exercise Days per Week (0-7): "))
        if exercise < 0 or exercise > 7:
            print("  ⚠️  Exercise days should be between 0-7")
            continue
        
        # Make prediction
        print("\n⏳ Processing...")
        prediction, confidence = predict_health_risk(age, bmi, smoker, exercise)
        
        if prediction is not None:
            # Display results
            print("\n" + "="*70)
            print("📊 PREDICTION RESULTS")
            print("="*70)
            
            # Risk level
            if prediction == 0:
                risk_status = "✅ LOW RISK"
                risk_advice = "Good news! Your health risk is LOW."
            else:
                risk_status = "⚠️  HIGH RISK"
                risk_advice = "Warning! Your health risk is HIGH."
            
            print(f"\nHealth Risk Status: {risk_status}")
            
            if confidence:
                print(f"Confidence Score: {confidence:.2%}")
            
            # Input summary
            print(f"\n📝 Your Inputs:")
            print(f"   Age: {age:.0f} years")
            print(f"   BMI: {bmi:.1f}")
            print(f"   Smoking: {smoker_str}")
            print(f"   Exercise: {exercise:.0f} days/week")
            
            # Health advice
            print(f"\n💡 Health Advice:")
            print(f"   {risk_advice}")
            
            if prediction == 0:
                print("""
   ✅ Recommendations:
      • Continue your healthy lifestyle
      • Maintain regular exercise routine
      • Keep monitoring your health metrics
      • Schedule regular health check-ups
                """)
            else:
                print("""
   ⚠️  Recommendations:
      • Consult with a healthcare professional
      • Consider lifestyle modifications
      • Increase exercise frequency
      • Monitor health metrics regularly
                """)
            
            print("="*70)
        
        else:
            print("\n❌ Error making prediction. Please try again.")
        
        # Ask if continue
        print("\n")
        again = input("Make another prediction? (yes/no): ").lower().strip()
        if again not in ['yes', 'y', '1']:
            print("\n✅ Thank you for using Health Risk Classification!")
            print("="*70 + "\n")
            break
    
    except ValueError:
        print("\n❌ Invalid input. Please enter valid numbers.")
    except KeyboardInterrupt:
        print("\n\n✅ Program stopped by user.")
        break
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please try again.")
