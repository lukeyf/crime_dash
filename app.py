import dash
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
from dash import html, dcc
from dash.dependencies import Input, Output, ClientsideFunction
import plotly.express as px
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt

import io
import pathlib

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
)
app.title = "Crime Rate Analytics Dashboard"
FACTOR_1 = 'population'
FACTOR_2 = 'violent_crime_rate'
server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("processed_communities.csv"))


state_list = df["state"].unique()
state_list = np.append('All', state_list,)
# df["Admit Source"] = df["Admit Source"].fillna("Not Identified")
community_list = df["area"].unique()
community_list = np.append(community_list, 'All')

column_list = {'latitude': 'Latitude',
               'longitude': 'Longitude',
               'population': 'Population',
               'PopDens': 'Population Density',
               'racepctblack': 'Black Race Percentage',
               'racePctWhite': 'White Race  Density',
               'racePctAsian': 'Asian Race  Density',
               'agePct12t29': 'Age Percentage (12-29)',
               'agePct65up': 'Age Percentage (65+)',
               'medIncome': 'Median Income',
               'violent_crime_rate': 'Violent Crime Rate',
               'NumStreet': 'Number of Streets',
               'PctUnemployed': 'Number of Unemployed'
               }


def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Crime Rate Analytics"),
            html.H3("Welcome to the Crime Rate Analytics Dashboard"),
            html.Div(
                id="intro",
                children="This is a dashboard for visualization of crime rate from a dataset collected in the 1990s. You can view the crime rate by zooming in on the US map, selecting desired state and community, and examine the correlation between factors and crime rates.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        style={"height": "100%", "width": "100%"},
        children=[

            html.P("Select State:"),
            dcc.Dropdown(
                id="state-select",
                options=[{"label": i, "value": i} for i in state_list],
                value='All',
            ),
            html.Br(),
            html.Br(),
            html.P("Select Analyzing Factor x:"),
            dcc.Dropdown(
                id="factor-select",
                options=[{"label": column_list[i], "value": i}
                         for i in column_list],
                value='population',
            ),
            html.Br(),
            html.P("Select Analyzing Factor y:"),
            dcc.Dropdown(
                id="factor-2-select",
                options=[{"label": column_list[i], "value": i}
                         for i in column_list],
                value='violent_crime_rate',
            ),
        ],
    )


app.layout = html.Div(
    id="app-container",
    children=[
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="us-map-section",
                    children=[

                        dcc.Tabs(id='tabs', value='tab-1', children=[
                            dcc.Tab(label='Interactive Map', value='tab-1', children=[
                                html.Div([
                                    html.B(
                                        "Interactive Map of Crime Rate in Communities of United States"),
                                    html.Hr(),
                                    dcc.Graph(id='map', figure={})
                                ])
                            ]),
                            dcc.Tab(label='Choropleth', value='tab-2', children=[
                                html.Div([
                                    html.B(
                                        "Average Crime Rate Categorized by State"),
                                    dcc.Graph(id='choropleth', figure={})
                                ])
                            ]),
                        ]),

                    ],
                ),
                html.Div(
                    id="scatter-section",
                    children=[
                        html.Br(),
                        html.Hr(),
                        html.B(
                            "Visualization of Correlation Analysis with Given Factor"),
                        html.Hr(),
                        dcc.Graph(id='scatter', figure={})
                    ]
                )
            ],
        ),
    ],
)


# Define the app callback
@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [
        Input("state-select", "value"),])
def update_figure(state):
    # Define the map figure
    filtered_df = df
    zoom = 3
    center = {
        'lat': 37,
        'lon': 180+80
    }
    if state != 'All' and state is not None:
        filtered_df = df[
            (df["state"] == state)
        ]
        x1, x2 = filtered_df['latitude'].min(), filtered_df['latitude'].max()
        y1, y2 = filtered_df['longitude'].min(), filtered_df['longitude'].max()
        max_bound = max(abs(x1-x2), abs(y1-y2)) * 111
        zoom = 11.5 - np.log(max_bound)
        center = None

    fig = px.scatter_mapbox(filtered_df,
                            lat="latitude",
                            lon="longitude",
                            center=center,
                            hover_name="area",
                            size='violent_crime_rate',
                            color='violent_crime_rate',
                            zoom=zoom, 
                            height=370,
                            labels = {
                                'violent_crime_rate':column_list['violent_crime_rate']
                            })

    # Update the layout of the figure
    fig.update_layout(mapbox_style="open-street-map",
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


@app.callback(
    Output("scatter", "figure"),
    [
        Input("state-select", "value"),
        Input("factor-select", "value"),
        Input("factor-2-select", "value"),
    ],
)
def update_scatter(state, column, column_2):
    global FACTOR
    filtered_df = df
    if state != 'All' and state is not None:
        filtered_df = df[
            (df["state"] == state)
        ]

    if column is None:
        column = FACTOR_1
    else:
        FACTOR_1 = column

    if column_2 is None:
        column_2 = FACTOR_2
    else:
        FACTOR_2 = column_2

    fig = px.scatter(filtered_df,
                     x=column,
                     y=column_2,
                     trendline="ols",
                     color=column_2,
                     trendline_color_override="black",
                     title="Correlation of "+column_list[column_2]+" versus " +
                     column_list[column],
                     hover_data=['area'],
                     labels={
                         column: column_list[column],
                         column_2: column_list[column_2],
                     })

    return fig


@app.callback(
    Output("choropleth", "figure"),
    [Input("state-select", "value"),]
)
def update_choropleth(state):
    filtered_df = df.groupby('state_abbrev').agg('mean').reset_index()
    fig = px.choropleth(locations=filtered_df['state_abbrev'], locationmode="USA-states",
                        color=filtered_df['violent_crime_rate'], scope="usa", height=350,
                        labels = {
                                'color':column_list['violent_crime_rate']
                            })
    fig.update_layout(mapbox_style="open-street-map",
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
