# #Importing Fastapi
from fastapi import FastAPI,Body
from fastapi.exceptions import HTTPException
import json

app = FastAPI()

#Htts Methods 1 - GET is used to fetch data or read data.
@app.get('/')
def greet():
    return "Hello World"

@app.get('/about')
def about():
    return "This is about Page"

@app.get('/feedback')
def feedback():
    return "This is feedback Page"

def load_data():
    with open('data.json','r') as fs:
        data = json.load(fs)
    return data

        

#endpoint -> data.json complete data dekhna hai
@app.get('/view')
def view():
    return load_data()

#Endpoint -> ek specific id ka data view kr paaye
@app.get('/view/{patient_id}')
def view_id(patient_id):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        return "Patient Not found"
    
def save_data(data):
    with open('data.json','w') as fs:
        json.dump(data,fs)

#Creating new patient by using POST
@app.post('/create/{patient_id}')
def create(patient_id:str,patient:dict=Body(...)):
    data =  load_data()
    if patient_id in data:
        raise HTTPException(status_code=400,detail="Patient already exist")
    data[patient_id] = patient
    save_data(data)


#Endpoint for updating patient.
@app.put('/edit/{patient_id}')
def edit(patient_id:str,update_data:dict=Body(...)):
    data = load_data()

    #Check if patient already exist or not.
    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient Not Found")

    #Existing patinet Data
    patient_data = data[patient_id]

    #update only provided data
    for key,value in update_data.items():
        patient_data[key] = value

    #Save data
    save_data(data)


#Endpoint for deleting record
@app.delete('/remove/{patient_id}')
def remove(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient Not Found")
    
    del data[patient_id]
    save_data(data)


from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
import pickle  # Use pickle to load your .pkl file
import json

app = FastAPI()

# 1. Define the input data format (Must match your model's training features)
class PatientFeatures(BaseModel):
    age: int
    bmi: float
    glucose: float
    # Add other features if your model was trained with them!

# 2. Load your model once at startup
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print("⚠️ Error: model.pkl not found in the directory.")

# --- NEW PREDICTION ENDPOINT ---
from pydantic import BaseModel

# This tells the API exactly what fields to show in the browser
class PatientData(BaseModel):
    age: int
    bmi: float

@app.post("/predict")
def predict(data: PatientData):
    # This takes the numbers you type in the browser
    input_data = [[data.age, data.bmi]]
    
    # This asks the model for the answer
    prediction = model.predict(input_data)
    
    return {"prediction": int(prediction[0])}

# --- YOUR EXISTING CODE (GREET, VIEW, ETC.) ---
@app.get('/')
def greet():
    return "Hello World - Prediction API is Live"

def load_data():
    with open('data.json','r') as fs:
        return json.load(fs)

@app.get('/view')
def view():
    return load_data()