import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import requests

# Loading model
try:
    model = pickle.load(open('/home/gustavo/Projects/CDS/DS_em_producao/model/model_rossmann.pkl', 'rb'))
except FileNotFoundError as e:
    print("Erro: Arquivo do modelo não encontrado:", e)
    exit(1)
except Exception as e:
    print("Erro ao carregar o modelo:", e)
    exit(1)

# initialize API
app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    try:
        test_json = request.get_json()

        if not test_json:
            return Response('{}', status=200, mimetype='application/json')

        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        # Instantiate Rossmann class
        pipeline = Rossmann()

        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)

        # feature engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response

    except Exception as e:
        print("Erro interno no servidor:", e)
        return Response('Erro interno no servidor', status=500)

if __name__ == '__main__':
    app.run('0.0.0.0')





