######################imports######################

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import pathlib
from app import app
import dash_table
from apps import reusableFunctions



######################data_import######################

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


df = pd.read_excel(DATA_PATH.joinpath(r'minaUtgifter.xlsx'))



######################columns etc######################


df['datum'] = pd.to_datetime(df['datum'])



df['str_date'] = df.datum.dt.strftime('%y-%B')
df['short_date'] = df.datum.dt.strftime('%y-%m')
df_group = df.groupby(['str_date', 'short_date', 'kategori']).sum()
df_group = df_group.reset_index(['str_date', 'short_date', 'kategori'])



kategori = ['Fest', 'Äta ute', 'Kläder', 'Inredning', 'Mat', 'Autogiro', 'Spara',
            'Semester', 'Teknik', 'Träningsredskap', 'Betting', 'Snus', 'Övrigt', 'Resa',
            'Lön', 'Hyra', 'Present']


month = df.drop_duplicates(['str_date','short_date'],ignore_index=True)[['str_date','short_date']].sort_values('short_date', ascending=True)



################define DF################


transactions = df.loc[:, ['short_date', 'beskrivning', 'summa', 'kategori']]


################sort values for presentation################

transactions = transactions.sort_values('short_date', ascending=True)




layout = html.Div(style = {}, children=[
    reusableFunctions.get_header(),
    reusableFunctions.get_navbar(),
    dash_table.DataTable(
        id='Transaktioner',
        columns=[{'name': i, 'id': i}
                 for i in transactions.columns],
        data=transactions.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )
])