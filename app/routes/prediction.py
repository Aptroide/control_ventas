# prediction.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
from datetime import datetime
from .. import schemas
import os


router = APIRouter(
    prefix="/predict",
    tags=["predicción"],
    responses={404: {"description": "No encontrado"}},
)

# Load the model at startup
try:
    model_path = os.path.join(os.path.dirname(__file__), 'prophet_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f'Error loading model: {e}')
    model = None

@router.post("/", response_model=schemas.PredictionResponse)
def make_prediction(pred_request: schemas.PredictionRequest):
    try:
        future = pd.DataFrame({'ds': [pred_request.fecha]})
        forecast = model.predict(future)
        pred = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].iloc[0].to_dict()
        return pred
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))