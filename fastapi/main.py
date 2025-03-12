from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# -------------------------
# Load trained models
# -------------------------
try:
    kmeans_model = joblib.load('kmeans.joblib')
    preprocessor_kmeans = joblib.load("scaler.joblib")
except Exception as e:
    raise RuntimeError(f"Error loading models: {str(e)}")

# -------------------------
# Define cluster mappings
# -------------------------
cluster_mapping_kmeans = {
    0: "Developing_Talents",
    1: "Team_Pillars",
    2: "Elite_Stars"
}

# -------------------------
# Define input schema
# -------------------------

class InputKMeans(BaseModel):
    minutes_played: int = Field(..., gt=0, description="Total minutes played by the player")
    appearance: int = Field(..., ge=0, description="Total number of appearances")
    highest_value: int = Field(..., gt=0, description="Highest market value of the player")

# -------------------------
# Feature Preprocessing Function for K-Means
# -------------------------

def preprocess_kmeans(input_features: InputKMeans):
    """
    Preprocesses input features for K-Means clustering:
    - Scales numerical features using StandardScaler
    """
    try:
        # Convert input into DataFrame
        input_df = pd.DataFrame([{
            "minutes played": input_features.minutes_played,
            "appearance": input_features.appearance,
            "highest_value": input_features.highest_value
        }])

        # Apply preprocessing pipeline
        scaled_features = preprocessor_kmeans.transform(input_df)
        return scaled_features

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {str(e)}")

# -------------------------
# K-Means Prediction Endpoint
# -------------------------

@app.post("/predict")
async def predict_kmeans(data: InputKMeans):
    """
    Predicts the cluster for K-Means based on input features.
    """
    try:
        # Preprocess the input
        scaled_input = preprocess_kmeans(data)

        # Predict cluster
        cluster_label = kmeans_model.predict(scaled_input)[0]
        cluster_name = cluster_mapping_kmeans.get(cluster_label, "Unknown Cluster")

        return {"cluster": int(cluster_label), "cluster_name": cluster_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
