import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


######################colors######################
######################colors######################
######################colors######################
######################colors######################

corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

######################Layouts######################
######################Layouts######################
######################Layouts######################
######################Layouts######################

graph_layout = go.Layout(
    paper_bgcolor= corporate_colors['superdark-green'],
    plot_bgcolor= corporate_colors['superdark-green'],
    xaxis= {'color' : corporate_colors['light-grey']},
    yaxis= {'color' : corporate_colors['light-grey']},
    title= {'font': {'color': corporate_colors['white'], 'size': 16}},
    font={'color': corporate_colors['light-grey']},
    title_x = 0.5
)




######################reusable functions######################
######################reusable functions######################
######################reusable functions######################
######################reusable functions######################



def get_header():

    header = html.Div([
        html.Div([], className='col-2'),
        html.Div([html.H1('Economic Dashboard', style={'color': 'white'})],style = {'padding-top' : '1%', 'textAlign': 'center'}, className='col-8'),
        html.Div([], className='col-2'),
    ],
        className='row',
        style={'height': '4%', 'background-color' : corporate_colors['superdark-green'],
               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}) #BOX-SHADOW DEFINES LINE

    return header



def get_navbar():

    navbar_summary = html.Div([
        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(html.H6(children='Economic Summary', style={'color': 'white', 'padding-top' : '5%', 'textAlign': 'center'})
                     , href='/apps/summary')], className='col-2'),
        html.Div([
            dcc.Link(html.H6(children='Transactions', style={'color': 'white', 'padding-top' : '5%', 'textAlign': 'center'})
                     , href='/apps/transactions')], className='col-2'),
        html.Div([
            dcc.Link(html.H6(children='Expenditures', style={'color': 'white', 'padding-top' : '5%', 'textAlign': 'center'})
                     , href='/apps/Monthly_expenditures')], className='col-2'),
        html.Div([], className='col-3')
    ], className='row',
    style={'background-color' : corporate_colors['dark-green']})



    return navbar_summary