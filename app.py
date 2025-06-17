from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
class UserInput(BaseModel):
    location:str
    total_sqft:float
    bathrooms:int
    bhk:int
    

with open('model/HomePricePrediction.pkl','rb') as f:
    model_data=pickle.load(f)
    
model= model_data['model']
columns = model_data['columns']
    
def predict_price(location, sqft, bath, bhk):
    try:
        loc_index = columns.index(location.lower())  # ensure lowercase
    except ValueError:
        loc_index = -1

    x = np.zeros(len(columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    return model.predict([x])[0]

app=FastAPI()
@app.get('/')
def index():
    return {'message':'Welcome To the House Price Prediction api'}

@app.post('/predict')
def predict(data:UserInput):
    predicted_price=predict_price(
        data.location, 
        data.total_sqft, 
        data.bathrooms, 
        data.bhk
    )
    return {'estimated_price_in_lakhs': round(float(predicted_price),2)}