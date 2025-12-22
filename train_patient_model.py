import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Simple data based on your data.json (Age, BMI) -> (0: Healthy, 1: Risk)
data = pd.DataFrame({
    'age': [35, 22, 40, 30, 21, 55, 60, 25],
    'bmi': [27.76, 17.58, 27.78, 31.22, 22.0, 35.0, 38.0, 21.0],
    'target': [1, 0, 0, 1, 0, 1, 1, 0]  # 1 means risk/overweight
})

X = data[['age', 'bmi']]
y = data['target']

model = RandomForestClassifier()
model.fit(X, y)

# Save it as model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Patient model created and saved as model.pkl")