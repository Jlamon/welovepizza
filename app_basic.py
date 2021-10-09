import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from file_uploaders import file_pizza_uploader, file_revenue_uploader
from graph_makers import mean_per_day_maker, mean_week_maker

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "27rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow-y": "auto"
}

# the styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "margin-top": "2rem",
    "padding": "2rem 1rem",
    "height": "95vh"
}

def get_visuals():
    visuals = [{'label': 'Moyenne par semaine', 'value': 'mean_week'},
               {'label': 'Moyenne par jours', 'value': 'mean_per_day'}]
    return visuals

sidebar = html.Div(
    [
        # html.H2("We Love Pizza Dashboard", className="display-6"),
        html.H2("Tester", className="display-6"),
        html.Hr(),
        html.P('Pick a graphical representation below.'),
        dbc.Select(
            id='visualselector',
            options=get_visuals(),
            value='mean_day',
            style={"margin-bottom": "10px"}
        ),
        dcc.Upload(
            id='upload-pizza',
            children=html.Div([
                dbc.Button("Upload Pizza File", id='upload-pizza-btn', outline=True, color="secondary", className="mr-1"),
                html.Div(id='error_pizza_message')
            ])
        ),
        # dcc.Upload(
        #     id='upload-revenue',
        #     children=html.Div([
        #         dbc.Button("Upload Revenue File", id='upload-revenue-btn', outline=True, color="secondary", className="mr-1"),
        #         html.Div(id='error_revenue_message')
        #     ])
        # ),
        html.Hr(),
        # dbc.Button("Refresh the network", id='change-btn', outline=True, color="secondary", className="mr-1"),
        html.P('By Julien Lamon', style={"margin-top": "10px"})
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [dcc.Graph(id='graphs')]
    , style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Callback for pizza file uploader
@app.callback(Output('error_pizza_message', 'children'),
              [Input('upload-pizza', 'contents')],
              [State('upload-pizza', 'filename')])
def upload_pizza_file(file_content, filename):
    return file_pizza_uploader(file_content, filename)

# Callback for revenue file uploader
# @app.callback(Output('error_revenue_message', 'children'),
#               [Input('upload-revenue', 'contents')],
#               [State('upload-revenue', 'filename')])
# def upload_revenue_file(file_content, filename):
#     return file_revenue_uploader(file_content, filename)

# Callback for graphs
@app.callback(Output('graphs', 'figure'), [Input('visualselector', 'value')])
def graph_maker(representation):
    if representation == 'mean_week':
        return mean_week_maker()
    else:
        return mean_per_day_maker()


if __name__ == '__main__':
    app.run_server(debug=True)
