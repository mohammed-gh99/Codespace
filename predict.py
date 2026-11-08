import pickle
import uvicorn
from fastapi import FastAPI
from typing import Dict, Any
# to tell FastAPI that the input is a dictionary with string keys and any type of values, we use Dict[str, Any]
from typing import Literal
from pydantic import BaseModel, Field
#now we define request , response and prediction models using Pydantic's BaseModel class. This allows us to define the structure of the data we expect to receive and send back in our API endpoints.

#request model
class Customer(BaseModel):
    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["no", "yes", "no_phone_service"]
    internetservice: Literal["dsl", "fiber_optic", "no"]
    onlinesecurity: Literal["no", "yes", "no_internet_service"]
    onlinebackup: Literal["no", "yes", "no_internet_service"]
    deviceprotection: Literal["no", "yes", "no_internet_service"]
    techsupport: Literal["no", "yes", "no_internet_service"]
    streamingtv: Literal["no", "yes", "no_internet_service"]
    streamingmovies: Literal["no", "yes", "no_internet_service"]
    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)",
    ]
    tenure: int = Field(..., ge=0)
    monthlycharges: float = Field(..., ge=0.0)
    totalcharges: float = Field(..., ge=0.0)

#response model
class PredictResponse(BaseModel):
    churn_probability: float
    churn: bool



app = FastAPI(title="churn-prediction")


with open('model.bin' , 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)

@app.post("/predict")
def predict(customer: Customer)-> PredictResponse:
    prob = predict_single(customer.model_dump())
    return PredictResponse(
        churn_probability= prob,
        churn= bool(prob >= 0.5)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)