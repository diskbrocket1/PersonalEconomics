import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import summary, transactions, monthexpen



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # html.Div([
    #     dcc.Link('Summary|', href='/apps/summary'),
    #     dcc.Link('Transactions|', href='/apps/transactions'),
    #     dcc.Link('Monthly_expenditures', href='/apps/Monthly_expenditures')
    # ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])


def display_page(pathname):
    if pathname == '/apps/summary':
        return summary.layout
    if pathname == '/apps/transactions':
        return transactions.layout
    if pathname == '/apps/Monthly_expenditures':
        return monthexpen.layout
    else:
        return summary.layout


if __name__ == '__main__':
    app.run_server(debug=False)