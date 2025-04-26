import pandas as pd
import joblib

class Model:
    def __init__(self):
        self.loaded_models = {}
        self.current_model = None
        self.current_model_feature = None
        self.df_encoded = None

    def load(self, name):
        if name not in self.loaded_models:
            model = joblib.load(f"models/{name}_model.pkl")
            model_features = joblib.load(f"models/{name}_features.pkl")
            self.loaded_models[name] = [model, model_features]

        self.current_model, self.current_model_feature = self.loaded_models[name]

    def preprocess_0(self, data):
        # This is used for ICU & Patient Type models
        feature_cols = self.current_model_feature
        transformed = {col: 0 for col in feature_cols}

        # AGE
        if 'AGE' in transformed:
            transformed['AGE'] = int(data.get('age', 0))

        # USMER
        usmer_value = data.get('usmer', '').lower()
        if 'USMER_1' in transformed and usmer_value == 'level_one':
            transformed['USMER_1'] = 1
        elif 'USMER_0' in transformed:
            transformed['USMER_0'] = 1

        # SEX
        sex_value = data.get('sex', '').lower()
        if 'SEX_1' in transformed and sex_value == 'female':
            transformed['SEX_1'] = 1
        elif 'SEX_0' in transformed:
            transformed['SEX_0'] = 1

        # COVID_status
        covid_value = data.get('covid_status', '').lower()
        if 'COVID_status_1' in transformed and 'positive' in covid_value:
            transformed['COVID_status_1'] = 1
        elif 'COVID_status_0' in transformed:
            transformed['COVID_status_0'] = 1

        # Binary yes/no health fields
        yes_no_fields = [
            ('asthma', 'ASTHMA'),
            ('cardiovascular', 'CARDIOVASCULAR'),
            ('copd', 'COPD'),
            ('diabetes', 'DIABETES'),
            ('hipertension', 'HIPERTENSION'),
            ('inmsupr', 'INMSUPR'),
            ('obesity', 'OBESITY'),
            ('other_disease', 'OTHER_DISEASE'),
            ('pneumonia', 'PNEUMONIA'),
            ('renal_chronic', 'RENAL_CHRONIC'),
            ('tobacco', 'TOBACCO')
        ]

        for raw_key, prefix in yes_no_fields:
            value = data.get(raw_key, '').lower()
            if f'{prefix}_1.0' in transformed and value == 'yes':
                transformed[f'{prefix}_1.0'] = 1
            elif f'{prefix}_0.0' in transformed:
                transformed[f'{prefix}_0.0'] = 1

        # PATIENT_TYPE
        if 'PATIENT_TYPE_0' in transformed or 'PATIENT_TYPE_1' in transformed:
            if 'patient_type' in data:
                val = data['patient_type'].lower()
                if 'outpatient' in val or 'returned home' in val:
                    if 'PATIENT_TYPE_0' in transformed:
                        transformed['PATIENT_TYPE_0'] = 1
                else:
                    if 'PATIENT_TYPE_1' in transformed:
                        transformed['PATIENT_TYPE_1'] = 1
            else:
                # Predicting patient type — use default
                if 'PATIENT_TYPE_0' in transformed:
                    transformed['PATIENT_TYPE_0'] = 1

        self.df_encoded = pd.DataFrame([transformed])
        # Debug print
        print("\nFinal Encoded DataFrame (preprocess_0):")
        for idx, row in self.df_encoded.iterrows():
            for col in self.df_encoded.columns:
                print(f"{col} = {row[col]}")


    def detect(self, model_name, data):
        self.load(model_name)

        self.preprocess_0(data)

        prediction = self.current_model.predict(self.df_encoded)[0]
        prediction_proba = self.current_model.predict_proba(self.df_encoded)[0]

        if model_name == "Patient Type":
            if prediction:
                prediction = "Returned Home"
            else:
                prediction = "Hospitalized"

        else:
            if prediction:
                prediction = "Yes"
            else:
                prediction = "No"

        proba_percentages = [str(round(float(prob) * 100, 2)) + "%" for prob in prediction_proba]

        return prediction, proba_percentages