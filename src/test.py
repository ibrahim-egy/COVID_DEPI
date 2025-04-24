import joblib
import pandas as pd

model = joblib.load("../models/Intubed_model.pkl")
model_features = joblib.load("../models/Intubed_features.pkl")

data = {
    "age": "3",
    "asthma": "Yes",
    "cardiovascular": "Yes",
    "copd": "Yes",
    "covid_status": "COVID_Positive",
    "diabetes": "Yes",
    "died": "Yes",
    "hypertension": "Yes",
    "inmsupr": "Yes",
    "obesity": "Yes",
    "other_disease": "Yes",
    "patient_type": "Home",
    "pneumonia": "Yes",
    "renal_chronic": "Yes",
    "sex": "Female",
    "tobacco": "Yes",
    "usmer": "Level_One"
}

df = pd.DataFrame([data])

# Ensure correct dtypes
for col in df.columns:
    if col != "age":
        df[col] = df[col].astype(str)
    else:
        df[col] = df[col].astype(float)  # age is numeric

# One-hot encode like training
df_encoded = pd.get_dummies(df)

# Align with model features (add missing columns as 0)
df_encoded = df_encoded.reindex(columns=model_features, fill_value=0)



prediction = model.predict(df_encoded)
prediction_proba = model.predict_proba(df_encoded)


print(prediction[0])
print(prediction_proba[0])
