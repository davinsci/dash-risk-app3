import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

key_dict = "/tmp/google_creds.json"
with open(key_dict, "w") as f:
    f.write(os.getenv("GOOGLE_CREDS"))
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(key_dict, scope)
client = gspread.authorize(creds)

# Setup
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Access Google Sheet
HSI = client.open_by_url("https://docs.google.com/spreadsheets/d/1D5V-B51Van2Vt1frrM8xkMyI9_3t-r26YFkuxv-B67M")

# Dataframe Setup
dfW = pd.DataFrame(HSI.worksheet('W3').get_all_records())

dfW['ALL 2'] = dfW['ALL']

Cats = ['Index 2','Type 2']

Figs = ['Index 2','Type 2',
        'ALL', 'A', 'J', 'O', 'M', 'Ml', 'Fl',
        'M A', 'M J', 'M O', 'M M', 'F A', 'F J', 'F O', 'F M',
        'ALL 2',
        'Z1', 'Z1 Ml', 'Z1 Fl', 'Z1 A', 'Z1 J', 'Z1 O', 'Z1 M', 
        'Z2', 'Z2 Ml', 'Z2 Fl', 'Z2 A', 'Z2 J', 'Z2 O', 'Z2 M', 
        'Z3', 'Z3 Ml', 'Z3 Fl', 'Z3 A', 'Z3 J', 'Z3 O', 'Z3 M', 
        'Z4', 'Z4 Ml', 'Z4 Fl', 'Z4 A', 'Z4 J', 'Z4 O', 'Z4 M', 
        ]

Figs4 = ['ALL','Male', 'Female',
         'Age 15-19','Male(15-19)','Female(15-19)',
         'Age 20-29','Male(20-29)','Female(20-29)',
         'Age 30-59','Male(30-59)','Female(30-59)', 
         'Age 60+', 'Male(60+)','Female(30-59)', 'Female(60+)'
        ]

Figs5 = ['ALL 2',
         'Zone 1', 'Zone 1 Male', 'Zone 1 Female', 'Zone 1 Age 15-19', 'Zone 1 Age 20-29','Zone 1 Age 30-59','Zone 1 Age 60+',
         'Zone 2', 'Zone 2 Male', 'Zone 2 Female', 'Zone 2 Age 15-19', 'Zone 2 Age 20-29','Zone 2 Age 30-59','Zone 2 Age 60+',
         'Zone 3', 'Zone 3 Male', 'Zone 3 Female', 'Zone 3 Age 15-19', 'Zone 3 Age 20-29','Zone 3 Age 30-59','Zone 3 Age 60+',
         'Zone 4', 'Zone 4 Male', 'Zone 4 Female', 'Zone 4 Age 15-19', 'Zone 4 Age 20-29','Zone 4 Age 30-59','Zone 4 Age 60+'
        ]

dfW = dfW[Figs]

# Column mapping
rename_map = {
    'ALL': 'ALL','A': 'Age 15-19', 'J': 'Age 20-29', 'O': 'Age 30-59', 'M': 'Age 60+', 
    'M A': 'Male(15-19)', 'M J': 'Male(20-29)', 'M O': 'Male(30-59)', 'M M': 'Male(60+)', 
    'F A': 'Female(15-19)', 'F J': 'Female(20-29)', 'F O': 'Female(30-59)', 'F M': 'Female(60+)', 
    'Ml': 'Male', 'Fl': 'Female',  'Z1': 'Zone 1', 'Z2': 'Zone 2', 'Z3': 'Zone 3', 'Z4': 'Zone 4', 
    'Z1 A':'Zone 1 Age 15-19', 'Z2 A':'Zone 2 Age 15-19', 'Z3 A':'Zone 3 Age 15-19', 'Z4 A':'Zone 4 Age 15-19', 
    'Z1 J':'Zone 1 Age 20-29', 'Z2 J':'Zone 2 Age 20-29', 'Z3 J':'Zone 3 Age 20-29', 'Z4 J':'Zone 4 Age 20-29', 
    'Z1 O':'Zone 1 Age 30-59', 'Z2 O':'Zone 2 Age 30-59', 'Z3 O':'Zone 3 Age 30-59', 'Z4 O':'Zone 4 Age 30-59', 
    'Z1 M':'Zone 1 Age 60+', 'Z2 M':'Zone 2 Age 60+', 'Z3 M':'Zone 3 Age 60+', 'Z4 M':'Zone 4 Age 60+', 
    'Z1 Ml':'Zone 1 Male', 'Z2 Ml':'Zone 2 Male', 'Z3 Ml':'Zone 3 Male', 'Z4 Ml':'Zone 4 Male', 
    'Z1 Fl':'Zone 1 Female', 'Z2 Fl':'Zone 2 Female', 'Z3 Fl':'Zone 3 Female', 'Z4 Fl':'Zone 4 Female'
}

dfW = dfW.rename(columns=rename_map, errors='ignore')

# Dataset Configuration
dfW = dfW.iloc[10:]
dfW = dfW.melt(id_vars=Cats, var_name='Category', value_name='Value')
dfW.loc[dfW['Category'].isin(Figs4), 'Index 2'] = 'W1'
dfW.loc[dfW['Category'].isin(Figs5), 'Index 2'] = 'W2'


windex = {}

for index_value in dfW["Index 2"].unique():
    windex[index_value] = dfW[dfW["Index 2"] == index_value]

W1 = windex["W1"].reset_index().copy()
W2 = windex["W2"].reset_index().copy()

W2['Category'] = W2['Category'].replace('ALL 2', 'ALL')

windex = {
    'W1': W1,
    'W2': W2
}

# Translated columns
for name, df in windex.items():
    df['Category (EN)'] = df['Category'].map({
            'ALL': 'All',
            'Male': 'Male','Female': 'Female',
            'Age 15-19': 'Age 15-19','Age 20-29': 'Age 20-29','Age 30-59': 'Age 30-59','Age 60+': 'Age 60+',
            'Male(15-19)': 'Male(15-19)','Male(20-29)': 'Male(20-29)',
            'Male(30-59)': 'Male(30-59)','Male(60+)': 'Male(60+)',
            'Female(15-19)': 'Female(15-19)','Female(20-29)': 'Female(20-29)',
            'Female(30-59)': 'Female(30-59)','Female(60+)': 'Female(60+)',
            'Zone 1': 'Northwest',
            'Zone 1 Male': 'Northwest Male','Zone 1 Female': 'Northwest Female',
            'Zone 1 Age 15-19': 'Northwest Age 15-19','Zone 1 Age 20-29': 'Northwest Age 20-29',
            'Zone 1 Age 30-59': 'Northwest Age 30-59','Zone 1 Age 60+': 'Northwest Age 60+',
            'Zone 2': 'Northeast',
            'Zone 2 Male': 'Northeast Male','Zone 2 Female': 'Northeast Female',
            'Zone 2 Age 15-19': 'Northeast Age 15-19','Zone 2 Age 20-29': 'Northeast Age 20-29',
            'Zone 2 Age 30-59': 'Northeast Age 30-59','Zone 2 Age 60+': 'Northeast Age 60+',
            'Zone 3': 'Southwest',
            'Zone 3 Male': 'Southwest Male','Zone 3 Female': 'Southwest Female',
            'Zone 3 Age 15-19': 'Southwest Age 15-19','Zone 3 Age 20-29': 'Southwest Age 20-29',
            'Zone 3 Age 30-59': 'Southwest Age 30-59','Zone 3 Age 60+': 'Southwest Age 60+',
            'Zone 4': 'Southeast',
            'Zone 4 Male': 'Southeast Male','Zone 4 Female': 'Southeast Female',
            'Zone 4 Age 15-19': 'Southeast Age 15-19','Zone 4 Age 20-29': 'Southeast Age 20-29',
            'Zone 4 Age 30-59': 'Southeast Age 30-59','Zone 4 Age 60+': 'Southeast Age 60+'
    })
    df['Category (ES)'] = df['Category'].map({
            'ALL':'Todo',
            'Male': 'Hombre','Female': 'Mujer',
            'Age 15-19': 'Edad 15-19','Age 20-29': 'Edad 20-29','Age 30-59': 'Edad 30-59','Age 60+': 'Edad 60+',
            'Male(15-19)': 'Hombre(15-19)','Male(20-29)': 'Hombre(20-29)',
            'Male(30-59)': 'Hombre(30-59)','Male(60+)': 'Hombre(60+)',
            'Female(15-19)': 'Mujer(15-19)','Female(20-29)': 'Mujer(20-29)',
            'Female(30-59)': 'Mujer(30-59)','Female(60+)': 'Mujer(60+)',
            'Zone 1': 'Norponiente',
            'Zone 1 Male': 'Norponiente Hombre','Zone 1 Female': 'Norponiente Mujer',
            'Zone 1 Age 15-19': 'Norponiente Edad 15-19','Zone 1 Age 20-29': 'Norponiente Edad 20-29',
            'Zone 1 Age 30-59': 'Norponiente Edad 30-59','Zone 1 Age 60+': 'Norponiente Edad 60+',
            'Zone 2': 'Nororiente',
            'Zone 2 Male': 'Nororiente Hombre','Zone 2 Female': 'Nororiente Mujer',
            'Zone 2 Age 15-19': 'Nororiente Edad 15-19','Zone 2 Age 20-29': 'Nororiente Edad 20-29',
            'Zone 2 Age 30-59': 'Nororiente Edad 30-59','Zone 2 Age 60+': 'Nororiente Edad 60+',
            'Zone 3': 'Surponiente',
            'Zone 3 Male': 'Surponiente Hombre','Zone 3 Female': 'Surponiente Mujer',
            'Zone 3 Age 15-19': 'Surponiente Edad 15-19','Zone 3 Age 20-29': 'Surponiente Edad 20-29',
            'Zone 3 Age 30-59': 'Surponiente Edad 30-59','Zone 3 Age 60+': 'Surponiente Edad 60+',
            'Zone 4': 'Suroriente',
            'Zone 4 Male': 'Suroriente Hombre','Zone 4 Female': 'Suroriente Mujer',
            'Zone 4 Age 15-19': 'Suroriente Edad 15-19','Zone 4 Age 20-29': 'Suroriente Edad 20-29',
            'Zone 4 Age 30-59': 'Suroriente Edad 30-59','Zone 4 Age 60+': 'Suroriente Edad 60+'
    })
    
    # Levels of Human Insecurity Intensity Measured by the Index
    df['VI (EN)'] = df['Type 2']
    df['VI (ES)'] = df['Type 2'].map({
        'Severe': 'Severa', 'Substantial': 'Sustancial', 'Moderate': 'Moderada', 'Mild': 'Leve'
    })
    
    df['VI_desc (EN)'] = df['VI (EN)'].map({
        'Severe': 'Vulnerability in the majority of dimensions, equivalent to having all priority dimensions affected.',
        'Substantial': 'Vulnerability in up to seven dimensions, but no more than three priority dimensions.',
        'Moderate': 'Up to six vulnerable dimensions, with no more than two of them being priority dimensions.',
        'Mild': 'No vulnerable priority dimensions and no more than one affected complementary dimension.'
    })
    
    df['VI_desc (ES)'] = df['VI (EN)'].map({
        'Severe': 'Vulnerabilidad en la mayoría de las dimensiones, que equivale a tener afectadas todas las dimensiones prioritarias.',
        'Substantial': 'Hasta siete dimensiones vulneradas, pero no más de tres de ellas son prioritarias.',
        'Moderate': 'Hasta seis dimensiones vulneradas, pero entre ellas no más de dos pueden ser prioritarias.',
        'Mild': 'No hay dimensiónes prioritarias vulneradas y como máximo una dimensión complementaria afectada.'
    })
    
translations = {
    '(EN)': {
        'title': 'Intensity of Human Insecurity',
        'yaxis': 'Percentage',
        'grouping': {'W1': 'By Age & Gender', 'W2': 'By Zone, Gender & Age'}
        },
    '(ES)': {
        'title': 'Intensidad de Inseguridad Humana',
        'yaxis': 'Porcentaje',
        'grouping': {'W1': 'Por Edad & Género', 'W2': 'Por Zona, Género & Edad'}
        }
}

vi_order = ['Severe', 'Substantial', 'Moderate', 'Mild']
vi_colors = {'Severe': 'red', 'Substantial': 'orange', 'Moderate': 'yellow', 'Mild': 'green'}

   
intro_descriptions = {
    '(EN)': "The index calculates the intensity of human insecurity experienced by each individual \
             based on the number and type of dimensions in which they have high levels of vulnerability.\
             The more dimensions that are affected, the greater the intensity of insecurity faced by the person. \
             While all dimensions are important and interrelated, the index recognizes that there are \
             four priority dimensions—personal security, economic security, food security, and health security—\
             which carry greater weight in the calculation of overall intensity.",
    '(ES)': "El índice calcula la intensidad de la inseguridad humana que experimenta cada persona, \
             según el número y tipo de dimensiones en las que ha tenido niveles medios, altos o extremos \
             de vulnerabilidad. Cuantas más dimensiones se encuentren afectadas, mayor será la intensidad de \
             inseguridad que enfrenta la persona. Si bien todas las dimensiones son importantes y están \
             interrelacionadas, el índice reconoce que hay cuatro dimensiones prioritarias —\
             seguridad personal, seguridad económica, seguridad alimentaria y seguridad en salud— \
             que tienen un peso mayor en el cálculo de la intensidad."
}

# Dash App
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(id='chart-title', style={'textAlign': 'center', 'fontFamily': 'Avenir Book'}),
    
    html.Div(id='intro-description', style={
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),
    
    html.Div([
        html.Label('Grouping:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='grouping-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Language:', style={'fontFamily': 'Avenir Book'}),
        dcc.RadioItems(
        id='language-select',
        options=[
        {'label': 'English', 'value': '(EN)'},
        {'label': 'Español', 'value': '(ES)'}
        ],
        value='(EN)',
        labelStyle={
        'display': 'inline-block',
        'padding': '6px 12px',
        'margin': '4px',
        'borderRadius': '5px',
        'border': '1px solid #ccc',
        'backgroundColor': '#f8f8f8',
        'cursor': 'pointer',
        'fontFamily': 'Avenir Book'
        },
        style={'fontFamily': 'Avenir Book'}
        )
    ], style={'width': '60%', 'margin': 'auto', 'padding': '20px'}),

    dcc.Graph(id='bar-chart')
], style={'fontFamily': 'Avenir Book'})

@app.callback(
    Output('grouping-select', 'options'),
    Output('grouping-select', 'value'),
    Input('language-select', 'value')
)
def update_dropdowns(lang):
    grouping_options = [{'label': translations[lang]['grouping'][k], 'value': k} for k in windex.keys()]
    return grouping_options, 'W1'

@app.callback(
    Output('bar-chart', 'figure'),
    Output('chart-title', 'children'),
    Output('intro-description', 'children'),
    Input('grouping-select', 'value'),
    Input('language-select', 'value')
)
def update_chart(grouping_key, lang):
    df = windex[grouping_key]
    df['Percentage'] = df['Value'] * 100
    df['VI_desc'] = df[f'VI_desc {lang}']
    df['VI_hover'] = df[f'VI {lang}'] + '<br>' + df['VI_desc']
    
    # Use translated columns
    x_column = 'Category ' + lang
    color_column = 'VI ' + lang

    # Build legend order and color map in target language
    vi_labels = [df[f'VI {lang}'][df['Type 2'] == vi].iloc[0] for vi in vi_order]
    color_map = {df[f'VI {lang}'][df['Type 2'] == vi].iloc[0]: vi_colors[vi] for vi in vi_order}

    fig = px.bar(
        df,
        x=x_column,
        y='Percentage',
        color=color_column,
        category_orders={color_column: vi_labels},
        color_discrete_map=color_map,
            text=df['Percentage'].round(1).astype(str) + '%',
        custom_data=['VI_hover'],
        hover_data=[]
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}<br>%{y}</b><br>%{customdata[0]}<extra></extra>')

    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title=translations[lang]['yaxis'],
            range=[0, 100],
            ticksuffix='%'
        ),
        title=dict(
            text=f"{translations[lang]['title']} ({translations[lang]['grouping'][grouping_key]})",
            x=0.5
        ),
        font=dict(
        family="Avenir Book",
        size=14,
        color='black'
        ),
        legend_title_text='',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    description = intro_descriptions[lang]

    return fig, translations[lang]['title'], description

if __name__ == '__main__':
    app.run_server(debug=False, port=8000, host='0.0.0.0')
