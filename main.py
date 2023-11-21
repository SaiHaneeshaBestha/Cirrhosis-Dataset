# Import packages
from dash import Dash, html, callback, Output, Input, State, dcc
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import dash_bootstrap_components as dbc

pipeline = pickle.load(open('best_model.pkl', 'rb+'))

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div([
            dbc.Label("Drug"),
            dcc.Dropdown(
                id="drug-dropdown",
                options=['D-penicillamine', 'Placebo'],
                value='D-penicillamine', clearable=False
            ),
            dbc.Label("AgeInYears"),
            dbc.Input(id="age-input", type="number", min=0, max=100, placeholder="Enter age"),
            dbc.Label("Sex"),
            dcc.Dropdown(
                id="sex-dropdown",
                options=['F', 'M'],
                value='M', clearable=False
            ),
            dbc.Label("Ascites"),
            dcc.Dropdown(
                id="ascites-dropdown",
                options=['Y', 'N'],
                value='Y', clearable=False
            ),
            dbc.Label("Hepatomegaly"),
            dcc.Dropdown(
                id="hepatomegaly-dropdown",
                options=['Y', 'N'],
                value='Y', clearable=False
            ),
            dbc.Label("Spiders"),
            dcc.Dropdown(
                id="spiders-dropdown",
                options=['Y', 'N'],
                value='Y', clearable=False
            ),
            dbc.Label("Bilirubin"),
            dbc.Input(id="bilirubin-input", type="number", placeholder="Enter Bilirubin value"),
            dbc.Label("Cholesterol"),
            dbc.Input(id="cholesterol-input", type="number", placeholder="Enter Cholesterol value"),
            dbc.Label("Albumin"),
            dbc.Input(id="albumin-input", type="number", placeholder="Enter Albumin value"),
            dbc.Label("Copper"),
            dbc.Input(id="copper-input", type="number", placeholder="Enter Copper value"),
            dbc.Label("Alk_Phos"),
            dbc.Input(id="alkphos-input", type="number", placeholder="Enter Alk_Phos value"),
            dbc.Label("SGOT"),
            dbc.Input(id="sgot-input", type="number", placeholder="Enter SGOT value"),
            dbc.Label("Tryglicerides"),
            dbc.Input(id="triglycerides-input", type="number", placeholder="Enter Tryglicerides value"),
            dbc.Label("Platelets"),
            dbc.Input(id="platelets-input", type="number", placeholder="Enter Platelets value"),
            dbc.Label("Prothrombin"),
            dbc.Input(id="prothrombin-input", type="number", placeholder="Enter Prothrombin value"),
            dbc.Button("Submit", id="submit-button", color="primary", className="mr-1"),
        ])
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="prediction-output"), width=12),
    ]),
])

# Callback to update the prediction
@app.callback(
    Output("prediction-output", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("drug-dropdown", "value"),
        State("age-input", "value"),
        State("sex-dropdown", "value"),
        State("ascites-dropdown", "value"),
        State("hepatomegaly-dropdown", "value"),
        State("spiders-dropdown", "value"),
        State("bilirubin-input", "value"),
        State("cholesterol-input", "value"),
        State("albumin-input", "value"),
        State("copper-input", "value"),
        State("alkphos-input", "value"),
        State("sgot-input", "value"),
        State("triglycerides-input", "value"),
        State("platelets-input", "value"),
        State("prothrombin-input", "value"),
    ],
)
def update_output(n_clicks, drug, age, sex, ascites, hepatomegaly, spiders, bilirubin, cholesterol, albumin, copper, alkphos, sgot, triglycerides, platelets, prothrombin):
    if n_clicks is None:
        return ""
    
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'Drug': [drug],
        'AgeInYears': [age],
        'Sex': [sex],
        'Ascites': [ascites],
        'Hepatomegaly': [hepatomegaly],
        'Spiders': [spiders],
        'Edema_N': [0],
        'Edema_S': [0],
        'Edema_Y': [0],
        'Bilirubin': [bilirubin],
        'Cholesterol': [cholesterol],
        'Albumin': [albumin],
        'Copper': [copper],
        'Alk_Phos': [alkphos],
        'SGOT': [sgot],
        'Tryglicerides': [triglycerides],
        'Platelets': [platelets],
        'Prothrombin': [prothrombin],
    })

    print(input_data.dtypes)
    # Make prediction
    prediction = pipeline.predict(input_data)[0]

    # Display prediction
    if prediction == 1:
        return "Patient is predicted to have cirrhosis."
    else:
        return "Patient is predicted not to have cirrhosis."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
