import pandas as pd
import joblib


class Model:
    def __init__(self):
        self.loaded_models = {}
        self.current_model = None
        self.current_model_feature = None
        self.current_df_scaled = None
        self.df_encoded = None

    def load(self, name):
        # Load model, and expected features
        model = joblib.load(f"models/{name}_model.pkl")
        model_features = joblib.load(f"models/{name}_features.pkl")

        self.loaded_models[name] = [model, model_features]

        self.current_model,self.current_model_feature = self.loaded_models[name]

    def preprocess(self, data):

        df = pd.DataFrame([data])

        for col in df.columns:
            if col != "age":
                df[col] = df[col].astype(str)
            else:
                df[col] = df[col].astype(float)  # age is numeric

        df_encoded = pd.get_dummies(df)

        self.df_encoded = df_encoded.reindex(columns=self.current_model_feature, fill_value=0)


    def detect(self, model_name, data):

        if model_name not in self.loaded_models:
            self.load(model_name)

        self.preprocess(data)

        prediction = self.current_model.predict(self.df_encoded)
        prediction_proba = self.current_model.predict_proba(self.df_encoded)

        return prediction[0], prediction_proba[0]
