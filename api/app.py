from fastapi import FastAPI

from src.predict import predict

app = FastAPI()

@app.get("/")
def home():

    return {
        "message": "Network Security ML API Running"
    }

@app.post("/predict")
def prediction(data: dict):

    result = predict(data)

    return {
        "prediction": result
    }