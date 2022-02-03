import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

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

## Subset to 2017, 2012
data_2017 = data[data['Year'] == 2017]
data_2012 = data[data['Year'] == 2012]

## Dictionary to map columns to cleaner version of the metric
titles_Dict = {'Animal_ag_share_no_feed': 'Agriculture Share, Excluding Feed Commodities',
                'Animal_ag_share_feed': 'Agriclutre Share, Including Feed Commodities',
                'Number_of_Family_Farmers': 'Family Farmers',
                'Farmers_in_animal_ag_no_feed': 'Animal Farmers, Excluding Feed Commodities',
                'Farmers_in_animal_ag_feed': 'Animal Farmers, Including Feed Commodities',
                'Total_Population': 'Total Population',
                'Total_Citizen_Population': 'Total Citizen Population',
                'Total_Registered': 'Total Registered Voters',
                'Percent_Registered_Total': 'Percent of Total that are registered to Vote',
                'Total_Registered_Margin_of_Error': 'Margin of Error for Total Registered Voters',
                'Percent_Registered_Citizen': 'Percent of Citizens that are registered to vote',
                'Citizen_Registered_Margin_of_Error': 'Margin of Error for Citizen Registered Voters',
                'Total_Voted': 'Total Votes casted',
                'Percent_Voted_Total': 'Percent of Total that voted',
                'Total_Voted_Margin_of_Error': 'Margin of Error for the total number of votes casted',
                'Percent_Voted_Citizen': 'Percent of Citizens that voted',
                'Citizen_Voted_Margin_of_Error': 'Margin of Error for the number of citizens that voted',
                'farmers_no_feed_per_person': 'Animal Farmers per Person, Excluding Feed Commodities',
                'farmers_feed_per_person': 'Animal Farmers per Person, Including Feed Commodities',
                'farmers_no_feed_per_voter': 'Animal Farmers per Voter, Excluding Feed Commodities',
                'farmers_feed_per_voter': 'Animal Farmers per Voter, Including Feed Commodities'
                }


###### CREATE FIGURE ######

# 2017 Data
fig1 = px.choropleth(data_2017,
    locations = 'code', # State Code for spatial coordinates
    color = 'Farmers_in_animal_ag_no_feed', # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    scope='usa',
    title="2017",
    labels={
        "Farmers_in_animal_ag_no_feed": "# of Farmers"
    },
    color_continuous_scale="speed"
)

buttons2017 = [dict(
                    args=[{'color': key}],
                    label=value,
                    method='update'
                ) for (key, value) in titles_Dict.items()]

fig1.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons2017,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.3,
            yanchor="top"
        ),
    ]
)

# 2012 Data
fig2 = px.choropleth(data_2012,
    locations = 'code', # State Code for spatial coordinates
    color = 'Farmers_in_animal_ag_no_feed', # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    scope='usa',
    title='2012',
    labels={
        "Farmers_in_animal_ag_no_feed": "# of Farmers"
    },
    color_continuous_scale="speed"
)

buttons2012 = [dict(
                    args=[{'color': key}],
                    label=value,
                    method='update'
                ) for (key, value) in titles_Dict.items()]

fig2.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons2012,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.3,
            yanchor="top"
        ),
    ]
)

###### END FIGURE ######


###### CREATE DASH APPLICATION ######

app = dash.Dash(__name__)

app.layout = html.Div( 
    children=[
        html.H1(
            children='Map Visualizations for the Ranchers Numbers Project',
            style={
                'textAlign': 'center',
                'color': 'white',
                'backgroundColor': 'darkcyan'
            }
        ),

        dcc.Graph(
            id='fig_2017',
            figure=fig1
        ),

        dcc.Graph(
            id='fig_2012',
            figure=fig2
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

###### END DASH APPLICATION ######

if __name__ == '__main__':
    app.run_server(debug=True)
