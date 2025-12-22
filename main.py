from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
import pickle
import json

app = FastAPI()

# 1. Load Model at startup
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# 2. Data Structures
class PatientData(BaseModel):
    age: int
    bmi: float

# --- ENDPOINTS ---

@app.get('/')
def greet():
    return "Hospital API is Live"

# Prediction (No Pandas used here to save space!)
@app.post("/predict")
def predict(data: PatientData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # We use a simple list of lists, which Scikit-Learn understands
    prediction = model.predict([[data.age, data.bmi]])
    return {"prediction": int(prediction[0])}

# Database logic
def load_data():
    with open('data.json','r') as fs:
        return json.load(fs)

def save_data(data):
    with open('data.json','w') as fs:
        json.dump(data,fs)

@app.get('/view')
def view():
    return load_data()

@app.post('/create/{patient_id}')
def create(patient_id:str, patient:dict=Body(...)):
    data = load_data()
    data[patient_id] = patient
    save_data(data)
    return {"status": "success"}
