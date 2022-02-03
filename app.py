########################################################

# DASH WEB APP FOR VISUALIZING RANCHER NUMBERS PROJECT
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

########################################################

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dictionaries import titles_Dict, legends_Dict

## Read in cleaned, (State, Year) - level data
data = pd.read_excel('data/family_farmer_estimates_state_year_level.xlsx')
data = data[data['State'] != "United States"] # only analyze every state
data['Year'] = data['Year'].astype(str)
# Join state codes
state_codes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv').loc[:, ['code', 'state']]
state_codes = state_codes.rename(columns = {'state': 'State'})
data = data.merge(state_codes, on='State')

###### COMPUTE NORMALIZATION METRICS #####
## farmers per person, no feed
data['farmers_no_feed_per_person'] = data['Farmers_in_animal_ag_no_feed'] / data['Total_Population']
## farmers per person, feed
data['farmers_feed_per_person'] = data['Farmers_in_animal_ag_feed'] / data['Total_Population']
## farmers per registered voter, no feed
data['farmers_no_feed_per_voter'] = data['Farmers_in_animal_ag_no_feed'] / data['Total_Registered']
## farmers per registered voter, feed
data['farmers_feed_per_voter'] = data['Farmers_in_animal_ag_feed'] / data['Total_Registered']
###### END NORMALIZATION METRICS ######

###### CREATE DASH APPLICATION ######
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div( 
    children=[
        # Header
        html.H1(
            children='Rancher Numbers Dashboard',
            style={
                'textAlign': 'center',
                'color': 'white',
                'backgroundColor': 'darkcyan'
            }
        ),
        # Map Description
        html.Div(
            children='Select a metric to visualize in the maps below', 
            style={
                'textAlign': 'left',
                'color': 'black',
                'backgroundColor': 'white'
            }
        ),
        # Map Dropdown
        dcc.Dropdown(
            id='map_dropdown',
            options=[{'label': v, 'value': k} for (k, v) in titles_Dict.items()],
            value="Farmers_in_animal_ag_no_feed"
        ),
        # Map
        html.Hr(),
        dcc.Graph(
            id='map_figure'
        ),
        # Map Description
        html.Div(
            children='Select a year and metric to sort in the table below:', 
            style={
                'textAlign': 'left',
                'color': 'black',
                'backgroundColor': 'white'
            }
        ),
        # Table Dropdown for Year
        dcc.Dropdown(
            id='table_year_dropdown',
            options=[{'label': y, 'value': y} for y in ['2017', '2012']],
            value="2017"
        ),
        # Table Dropdown for columns
        dcc.Dropdown(
            id='table_value_dropdown',
            options=[{'label': v, 'value': k} for (k, v) in titles_Dict.items()],
            value="Farmers_in_animal_ag_no_feed"
        ),
        # Table
        dcc.Graph(
            id='table_figure'
        ),
        # Bottom Text
        html.Div(
            children=[
                html.Label(
                    children='The data used to generate these maps is public available through the U.S. Department of Agriculture and the U.S. Census Bureau.', 
                    style={
                        'textAlign': 'left',
                        'color': 'black',
                        'backgroundColor': 'white'
                    }
                ),
                html.Label(
                    children = ['  For an overview of the project, and for details on how some of these metrics were calculated, refer to this ', 
                        html.A('repository', 
                        href='/https://github.com/Kendall-Kikkawa/GFI_rancher_project'),
                        "."
                    ],
                    style={
                        'color': 'black',
                        'backgroundColor': 'white'
                    }
                ),
                html.Label(
                    children = ['  This project was conducted in collaboration with the ', 
                        html.A('Good Food Institute', 
                        href='/https://gfi.org/'),
                        "."
                    ],
                    style={
                        'color': 'black',
                        'backgroundColor': 'white'
                    }
                )
            ]
        )
    ]
)

@app.callback(
    dash.dependencies.Output('map_figure', 'figure'),
    [dash.dependencies.Input('map_dropdown', 'value')])
def update_map(value):
    """
    Updates the Map based upon the desired quantity to plot - the figure plots the value in each state of
    the U.S. in the years 2017 and 2012

    Args:
        value (string): String describing the metric to be plotted

    Returns:
        figure (px.Figure): figure to be displayed on the Dash app
    """
    fig = px.choropleth(data,
        locations = 'code', # State Code for spatial coordinates
        color = value, # Data to be color-coded
        facet_col='Year',
        locationmode = 'USA-states', # set of locations match entries in `locations`
        scope='usa',
        title=titles_Dict[value],
        labels={
            value: legends_Dict[value]
        },
        color_continuous_scale="speed"
    )
    return fig


@app.callback(
    dash.dependencies.Output('table_figure', 'figure'),
    [dash.dependencies.Input('table_year_dropdown', 'value'), 
    dash.dependencies.Input('table_value_dropdown', 'value')])
def update_table(year, value):
    """
    Updates the Table based upon the desired quantity to sort on, drops all other columns
    - rearranges table so that sorted table goes 3rd (after State, code)

    Args:
        value (string): String describing the metric to be plotted

    Returns:
        figure (px.Figure): table to be displayed on the Dash app
    """
    year_data = data[data['Year'] == year]
    year_data = year_data.reset_index()
    year_data = year_data.drop(columns=['Year'])
    # Shift code and value columns
    code_col = year_data.pop('code')
    year_data.insert(1, 'code', code_col)
    value_col = year_data.pop(value)
    year_data.insert(2, value, value_col)
    # Drop all other columns
    year_data = year_data.loc[:, ['State', 'code', value]]
    year_data = year_data.sort_values(by=[value], ascending=False)
    year_data[value] = year_data[value].round(4)

    fig = go.Figure()
    fig.add_table(cells=dict(
                        values=[year_data[col].tolist() for col in ['State', 'code', value]]
                        ), 
                  header=dict(values=['State', 'State Code', titles_Dict[value]]), 
                 )

    return fig

###### END DASH APPLICATION ######


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
