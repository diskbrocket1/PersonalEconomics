######################imports######################

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import pathlib
from app import app
import plotly.express as px
from apps import reusableFunctions



######################data_import######################

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


df = pd.read_excel(DATA_PATH.joinpath(r'minaUtgifter.xlsx'))


######################columns etc######################


df['datum'] = pd.to_datetime(df['datum'])



df['short_date'] = df.datum.dt.strftime('%y-%m')
df_group = df.groupby(['short_date', 'kategori']).sum()
df_group = df_group.reset_index(['short_date', 'kategori'])



kategori = ['Fest', 'Äta ute', 'Kläder', 'Inredning', 'Mat', 'Autogiro', 'Spara',
            'Semester', 'Teknik', 'Träningsredskap', 'Betting', 'Snus', 'Övrigt', 'Resa',
            'Lön', 'Hyra', 'Present']


month = df.short_date
month = month.drop_duplicates().sort_values(ascending=True)
month_dict = {k:v for k,v in enumerate(month)}


################define DF################

expenses = df_group[-df_group['kategori'].isin(['Lön','Spara'])]
expenses_new = expenses.copy()
expenses_new['summa'] = expenses_new['summa']*-1
expenses_annotation = expenses_new.groupby(['short_date']).sum('summa').reset_index(['short_date'])





################colors for graphs################
colors_id = ['#1C4E80', 'aquamarine', '#0091D5','#EA6A47', 'bisque', '#DBAE58',
             '#523f6d', '#a3b745', '#d46f15', '#e2d337', '#5e5f37', '#ec90ad',
             '#a47668', '#17937e', '#09d350', '#be22a0', 'aquamarine']
zip_list = zip(kategori, colors_id)
color_dict = dict(zip_list)




######################app_dash######################



layout = html.Div(style = {}, children=[
    reusableFunctions.get_header(),
    reusableFunctions.get_navbar(),
    html.Div([
        html.Div([], className='col-1'),
        html.Div([dcc.Dropdown(id='month', style={}, options=[{'label': i, 'value': i} for i in month],value=month[0])], className='col-2'),
    ], className='row',
    style={'background-color': reusableFunctions.corporate_colors['dark-green']}),
    html.Div([
        html.Div([], className='col-1'),
        html.Div([
            html.Div([
            html.Div([dcc.Graph(id='expenses_per_month')], className='col-7'),
            html.Div([dcc.Graph(id='expenses_per_month_pie')], className='col-5')
        ], className='row',
            style={'background-color' : reusableFunctions.corporate_colors['superdark-green']})
        ], className='col-10'),
        html.Div([], className='col-1')
    ],
    className='row',
    style={'background-color': reusableFunctions.corporate_colors['dark-green']}),

    html.Div([
        html.Div([], className='col-1'),
        html.Div([dcc.Graph(id='monthly_expenses')], className='col-10'),
        html.Div([], className='col-1')
    ], className='row',
    style={'background-color': reusableFunctions.corporate_colors['dark-green']}),


    html.Div([
        html.Div([], className='col-1'),
        html.Div(dcc.RangeSlider('summary_slider',
                        min=0,
                        max=len(month)-1,
                        step=None,
                        marks=month_dict,
                        value=[0,1]), className='col-10'),
        html.Div([], className='col-1'),
    ], className='row',
    style={'background-color' : reusableFunctions.corporate_colors['dark-green']}),
    html.Div([
    html.Div([
        html.Br()],
        className='col-12')], className='row', style={'height': '45px','background-color' : reusableFunctions.corporate_colors['dark-green']})
])





@app.callback(
    Output(component_id='expenses_per_month', component_property='figure'),
    Output(component_id='expenses_per_month_pie', component_property='figure'),
    Output(component_id='monthly_expenses', component_property='figure'),
    Input(component_id='month', component_property='value'),
    Input(component_id='summary_slider', component_property='value')
)

def update_graph(months, value):

    if min(expenses_new[expenses_new['short_date']==months]['summa']) >= 0:
        x_min = 0
    else:
        x_min = min(expenses_new[expenses_new['short_date']==months]['summa']) - 200

    x_max = max(expenses_new[expenses_new['short_date']==months]['summa'])+200


    colors = [color_dict[k] for k in expenses_new[expenses_new['short_date']==months]['kategori']]


    fig = go.Figure(go.Bar(x=expenses_new[expenses_new['short_date']==months]['summa'],
                           y=expenses_new[expenses_new['short_date']==months]['kategori'],
                           orientation='h',
                           marker_color=colors),
                    layout=reusableFunctions.graph_layout)
    fig.update_layout(yaxis={'title': 'Kategori'},
                      xaxis={'range': [x_min,x_max], 'showticklabels':False},
                      title= {'text': 'Absolute expenditures during {})'.format(months)},
                      uniformtext_minsize=12,
                      uniformtext_mode='show',
                       annotations=[
                           dict(
                               x=1.15,
                               xref='paper',
                               y=row.kategori,
                               text='{} SEK'.format(round(row.summa)),
                               showarrow=False,
                           ) for index, row in expenses_new[expenses_new['short_date']==months].iterrows()
                       ])

##################### #####################

    monthly_expenses_pie = go.Figure(go.Pie(labels=expenses_new[expenses_new['short_date']==months]['kategori'],
                                            values=expenses_new[expenses_new['short_date']==months]['summa']),
                                     layout=reusableFunctions.graph_layout)
    monthly_expenses_pie.update_layout(title={'text': 'Categorical allocation of expenditures'})

##################### #####################
    first = value[0]
    last = value[1]+1

    month_temp = [month_dict[x] for x in list(range(first,last))]
    monthly_expenses_temp = expenses_new[expenses_new['short_date'].isin(month_temp)]
    expenses_annotation_temp = expenses_annotation[expenses_annotation['short_date'].isin(month_temp)]

    monthly_expenses_temp = monthly_expenses_temp.groupby('kategori')


    monthly_expenses = go.Figure(
        data=[
            go.Bar(name=kategori, x=group.short_date, y=group.summa) for kategori, group in monthly_expenses_temp
        ], layout=reusableFunctions.graph_layout)

    monthly_expenses.update_layout(barmode='stack',
                                   annotations=[dict(
                                       x = row.short_date,
                                       y = 1.05,
                                       yref='paper',
                                       text = '{} SEK'.format(round(row.summa)),
                                       showarrow=False
                                   ) for index, row in expenses_annotation_temp.iterrows()],
                                   yaxis={'title': 'SEK'},
                                   title={'text': 'Monthly Expenditures in SEK'},
                                   xaxis={'tickvals': month_temp, 'title': 'Month'}
                                   )





    return [fig, monthly_expenses_pie, monthly_expenses]

