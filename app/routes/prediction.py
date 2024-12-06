# prediction.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
from datetime import datetime
from .. import schemas

router = APIRouter(
    prefix="/predict",
    tags=["predicción"],
    responses={404: {"description": "No encontrado"}},
)

# Cargar el modelo al iniciar
with open('/home/runner/work/control_ventas/control_ventas/prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)

@router.post("/", response_model=schemas.PredictionResponse)
def make_prediction(pred_request: schemas.PredictionRequest):
    try:
        future = pd.DataFrame({'ds': [pred_request.fecha]})
        forecast = model.predict(future)
        pred = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].iloc[0].to_dict()
        return pred
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))