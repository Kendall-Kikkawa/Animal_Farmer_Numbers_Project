########################################################

# DASH WEB APP FOR VISUALIZING RANCHER NUMBERS PROJECT
# Run this app with `python app.py` and
# visit http://0.0.0.0:8050/ in your web browser.

########################################################

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dictionaries import titles_Dict, legends_Dict

## Read in cleaned, (State, Year) - level data
data = pd.read_excel('data/family_farmer_estimates_state_year_level.xlsx')
data = data[data['State'] != "United States"] # only analyze every state
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

app.layout = html.Div( 
    children=[
        html.H1(
            children='Map Visualizations for the Rancher Numbers Project',
            style={
                'textAlign': 'center',
                'color': 'white',
                'backgroundColor': 'darkcyan'
            }
        ),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': v, 'value': k} for (k, v) in titles_Dict.items()],
            value="Farmers_in_animal_ag_no_feed"
        ),
        html.Hr(),
        dcc.Graph(
            id='fig'
        ),
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
                        ".  '[Google](https://www.google.com)'   "
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
    dash.dependencies.Output('fig', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    """
    Updates the Figure based upon the desired quantity to plot - the figure plots the value in each state of
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

###### END DASH APPLICATION ######

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
