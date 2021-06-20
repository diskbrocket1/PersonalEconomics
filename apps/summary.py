######################imports######################

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import pathlib
from app import app
import dash_table
import plotly.express as px
from apps import reusableFunctions




######################data_import######################
######################data_import######################
######################data_import######################
######################data_import######################


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


df = pd.read_excel(DATA_PATH.joinpath(r'minaUtgifter.xlsx'))


###################### datum ######################
###################### datum ######################
###################### datum ######################
###################### datum ######################

df['datum'] = pd.to_datetime(df['datum'])
df['short_date'] = df.datum.dt.strftime('%y-%m')
df['year'] = df.datum.dt.strftime('%y')


month = df.short_date
month = month.drop_duplicates().sort_values(ascending=True)
month_dict = {k:v for k,v in enumerate(month)}

###################### group main DF ######################
###################### group main DF ######################
###################### group main DF ######################
###################### group main DF ######################

df_group = df.groupby(['year', 'short_date', 'kategori']).sum()
df_group = df_group.reset_index(['year', 'short_date', 'kategori'])


################ define monthly DFs ################
################ define monthly DFs ################
################ define monthly DFs ################
################ define monthly DFs ################


monthly_resultat = df_group[-df_group['kategori'].isin(['Spara'])].groupby(['short_date']).sum('summa').reset_index(['short_date'])
monthly_resultat['kategori'] = 'Result'
monthly_exp = df_group[-df_group['kategori'].isin(['Spara','Lön'])].groupby(['short_date']).sum('summa').reset_index(['short_date'])
monthly_exp['summa'] = monthly_exp['summa']*-1
monthly_exp['kategori'] = 'Expenses'
monthly_salary = df_group[df_group['kategori'].isin(['Lön'])].groupby(['short_date']).sum('summa').reset_index(['short_date'])
monthly_salary['kategori'] = 'Salary'

#append
monthly_summary = pd.DataFrame()
monthly_summary = monthly_summary.append([monthly_resultat,monthly_exp,monthly_salary])


################ define yearly DF ################
################ define yearly DF ################
################ define yearly DF ################
################ define yearly DF ################


yearly_res = df_group[-df_group['kategori'].isin(['Spara'])].groupby(['year']).sum('summa').reset_index(['year'])


######################app_dash######################
######################app_dash######################
######################app_dash######################
######################app_dash######################


layout = html.Div(style = {}, children=[
    reusableFunctions.get_header(),
    reusableFunctions.get_navbar(),
    html.Div([
        html.Div([], className='col-2'),
        html.Div(dcc.Graph(id='summary'), className='col-8'),
        html.Div([], className='col-2')
    ],
        className='row',
    style={'background-color' : reusableFunctions.corporate_colors['dark-green']}),
    html.Div([
        html.Div([], className='col-2'),
        html.Div(dcc.RangeSlider('summary_slider',
                        min=0,
                        max=len(month)-1,
                        step=None,
                        marks=month_dict,
                        value=[0,0]), className='col-8'),
        html.Div([], className='col-2'),
    ], className='row',
    style={'background-color' : reusableFunctions.corporate_colors['dark-green']}),
    html.Div([
        html.Div([], className='col-2'),
        html.Div(dcc.Graph(id='result'), className='col-8'),
        html.Div([], className='col-2')
    ], className='row',
    style={'background-color' : reusableFunctions.corporate_colors['dark-green']})

])



@app.callback(
    Output(component_id='summary', component_property='figure'),
    Output(component_id='result', component_property='figure'),
    Input(component_id='summary_slider', component_property='value')
)

def slider_chart(value):

    first = value[0]
    last = value[1]+1

    dates = [month_dict[x] for x in list(range(first,last))]

    summary_temp = monthly_summary[monthly_summary['short_date'].isin(dates)]
    summary_temp['summa'] = round(summary_temp['summa'], 0)
    summary_temp = summary_temp.groupby('kategori')



    fig_summary_mm = go.Figure(
        data=[
            go.Bar(name=kategori, x=group.short_date, y=group.summa) for kategori, group in summary_temp
        ], layout=reusableFunctions.graph_layout
    )
    fig_summary_mm.update_layout(barmode='group', xaxis= {'tickvals': dates, 'title': 'Month'},
                                 yaxis={'title': 'SEK'}, title= {'text': 'Monthly Result in SEK'})



    fig_yearly = go.Figure(go.Bar(x = yearly_res['year'],
                        y = yearly_res['summa'],
                        width=0.1), layout=reusableFunctions.graph_layout)
    fig_yearly.update_layout(xaxis= {'title': 'År', 'tickvals': yearly_res.drop_duplicates(['year'])['year']},
                             yaxis= {'title': 'Årligt resultat'}, title={'text': 'Yearly Result'})

    return [fig_summary_mm, fig_yearly]