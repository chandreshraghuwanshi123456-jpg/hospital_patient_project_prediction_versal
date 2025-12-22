import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Hospital AI Predictor")

st.title("🏥 Hospital Patient Risk Prediction")
st.write("Enter patient details below to get an instant health risk assessment.")

# 1. Create Input Fields
# These match the 'age' and 'bmi' your FastAPI expects
age = st.slider("Patient Age", min_value=1, max_value=120, value=30)
bmi = st.number_input("Patient BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)

# 2. Add a Prediction Button
if st.button("Run Diagnostic Analysis"):
    # The URL of your LOCAL FastAPI server
    api_url = "http://127.0.0.1:8000/predict"
    
    # Prepare the data to send
    payload = {
        "age": age,
        "bmi": bmi
    }
    
    try:
        # Send data to FastAPI
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            result = response.json().get("prediction")
            
            # 3. Display Results Nicely
            if result == 1:
                st.error("⚠️ High Risk Detected: Follow-up recommended.")
            else:
                st.success("✅ Low Risk: Patient parameters appear normal.")
        else:
            st.error(f"API Error: Received status code {response.status_code}")
            
    except Exception as e:
        st.error(f"Could not connect to the Backend. Is Uvicorn running? Error: {e}")