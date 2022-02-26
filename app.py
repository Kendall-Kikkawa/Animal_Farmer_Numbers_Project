########################################################

# DASH WEB APP FOR VISUALIZING RANCHER NUMBERS PROJECT
# Run this app with `python3 app.py` and
# visit http://0.0.0.0:8050/ in your web browser.

########################################################

from turtle import width
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
            children='Animal Farmers Dashboard',
            style={
                'textAlign': 'center',
                'color': 'white',
                'backgroundColor': 'darkcyan',
                "padding-top": "10px",
                "padding-bottom": "10px",
            }
        ),
        # Description
        html.H2(
            children='Project Overview',
            style={
                'textAlign': 'left',
                'color': 'Black',
                'backgroundColor': 'white',
                'margin-top': '3px',
                'margin-bottom': '3px'
            }
        ),
        html.Div(
            children=[
                html.Label(
                    children = [
                        'This dashboard provides estimates of the number of individuals and family-owned farmers involved in animal agriculture by U.S. state in 2012 and 2017. ',
                        'The data used com from multiple sources: the Economic Research Service of the U.S. Department of Agriculture (', 
                        dcc.Link('ERS data', href='https://data.ers.usda.gov/reports.aspx?ID=17832'),
                        ')  the Natural Agricultural Statistics Service of the U.S.D.A. (',
                        dcc.Link('NASS data', href='https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1'),
                        ') and the U.S. Census Bureau Current Population Surveys (',
                        dcc.Link('2018 CPS', href='https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-583.html'),
                        ', ',
                        dcc.Link('2012 CPS', href='https://www.census.gov/data/tables/2012/demo/voting-and-registration/p20-568.html'),
                        '). The dashboard computes two estimates of this measure: including and excluding feed commodities.'
                    ],
                ),
                html.Div(
                    children=[
                        ' ',
                        html.Br(),
                        'We made the following proportionality assumptions due to the lack of specific data:',
                        dcc.Markdown('''
                                    1. Ratio of animal agriculture revenue in total agriculture revenue in the state is proportional to that ratio among individual and family farmers.
                                    2. Proportion of individual and family farmers that vote is the same as average in the state.
                                    3. We count each individual and family farm as ONE person - if you believe that the right number is N>1, multiply all reported numbers for family farmers by N.
                                '''),
                        html.Label(
                            children = ['For additional details on this project and on how some of these metrics were calculated, refer to the ', 
                                dcc.Link('project repository', href='https://github.com/Kendall-Kikkawa/GFI_rancher_project'),
                                "."
                            ]
                        )
                    ]
                )
            ],
            style={
                'color': 'black',
                'display': 'inline-block',
                'backgroundColor': 'ghostwhite',
                "padding-top": "15px",
                "padding-bottom": "15px",
            }
        ),
        html.Div('_',
            style={
                    'color': 'white',
                    'display': 'inline-block',
                    'backgroundColor': 'white'
                }
        ),
        html.Hr(),        
        # Map Dropdown
        html.H2(
            children='Select a metric to visualize in the maps and tables below', 
            style={
                'textAlign': 'left',
                'color': 'black',
                'backgroundColor': 'white'
            }
        ),
        dcc.Dropdown(
            id='map_dropdown',
            options=[{'label': v, 'value': k} for (k, v) in titles_Dict.items()],
            value="Farmers_in_animal_ag_no_feed"
        ),
        html.Div(
            children='_', 
            style={
                'textAlign': 'left',
                'color': 'white',
                'backgroundColor': 'white'
            }
        ),
        html.Hr(),
        # 2017 Header
        html.H2(
            children=[
                'Distribution of ',
                html.Div(id='selected_metric_2017'),
                ' by state in 2017'],
            style={
                'textAlign': 'left',
                'color': 'black',
                'backgroundColor': 'white',
                'margin-top': '10px',
                'margin-bottom': '3px'
            }
        ),
        # 2017 Map and Table
        html.Div([ 
            html.Div(children=dcc.Graph(id='map_figure_2017',
                                        figure={"layout": {"height": 355}}), 
                style={
                    'width': '48%',
                    'height': '100%',
                    'display': 'inline-block',
                    "padding-left": "5px",
                    "padding-right": "5px",
                    "padding-top": '2px',
                    "padding-bottom": '2px'}),
            html.Div(children=dcc.Graph(id='table_figure_2017',
                                        figure={"layout": {"height": 355}}),
                style={
                    'width': '48%',
                    'height': '100%',
                    'display': 'inline-block',
                    "padding-left": "5px",
                    "padding-right": "5px",
                    "padding-top": '2px',
                    }),
        ],
        style={
            'textAlign': 'center'
        }),
        # 2012 Header
        html.H2(
            children=[
                'Distribution of ',
                html.Div(id='selected_metric_2012'),
                ' by state in 2012'],
            style={
                'textAlign': 'left',
                'color': 'black',
                'backgroundColor': 'white',
                'margin-top': '3px',
                'margin-bottom': '3px'
            }
        ),
        # 2012 Map and Table
        html.Div([ 
            html.Div(children=dcc.Graph(id='map_figure_2012',
                                        figure={"layout": {"height": 355}}), 
                style={
                    'width': '48%',
                    'height': '100%',
                    'display': 'inline-block',
                    "padding-left": "5px",
                    "padding-right": "5px",
                    "padding-top": '2px'}),
            html.Div(children=dcc.Graph(id='table_figure_2012',
                                        figure={"layout": {"height": 355}}), 
                style={
                    'width': '48%',
                    'height': '100%',
                    'display': 'inline-block',
                    "padding-left": "5px",
                    "padding-right": "5px",
                    "padding-top": '2px'}),
        ],
        style={
            'textAlign': 'center'
        })
    ]
)


@app.callback(
    dash.dependencies.Output('selected_metric_2017', 'children'),
    dash.dependencies.Output('selected_metric_2012', 'children'),
    [dash.dependencies.Input('metric_string', 'value')]
)
def get_metric(value):
    """Gets selected metric to update titles for maps and tables

    Args:
        value (string): String describing the metric to be plotted

    Returns:
        (string): Clean version of string describing the metric to be plotted, unique for 2017 plots
        (string): Clean version of string describing the metric to be plotted, unique for 2012 plots
    """
    return titles_Dict[value], titles_Dict[value]


@app.callback(
    dash.dependencies.Output('map_figure_2012', 'figure'),
    dash.dependencies.Output('map_figure_2017', 'figure'),
    [dash.dependencies.Input('map_dropdown', 'value')])
def update_map(value):
    """
    Updates the Map based upon the desired quantity to plot - the figure plots the value in each state of
    the U.S. in the years 2017 and 2012

    Args:
        value (string): String describing the metric to be plotted

    Returns:
        map_figure_2012 (px.Figure): 2012 map to be displayed on the Dash app
        map_figure_2017 (px.Figure): 2017 map to be displayed on the Dash app
    """
    # 2012 Map
    data_2012 = data[data['Year'] == '2012']
    fig_2012 = px.choropleth(data_2012,
        locations = 'code', # State Code for spatial coordinates
        color = value, # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        scope='usa',
        labels={
            value: legends_Dict[value]
        },
        color_continuous_scale="speed",
    )
    fig_2012.update_layout(margin=dict(r=10, l=10, t=10, b=10),
                            paper_bgcolor="ghostwhite")

    # 2017 Map
    data_2017 = data[data['Year'] == '2012']
    fig_2017 = px.choropleth(data_2017,
        locations = 'code', # State Code for spatial coordinates
        color = value, # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        scope='usa',
        labels={
            value: legends_Dict[value]
        },
        color_continuous_scale="speed",
    )
    fig_2017.update_layout(margin=dict(r=10, l=10, t=10, b=10),
                            paper_bgcolor="ghostwhite")

    return fig_2012, fig_2017


@app.callback(
    [dash.dependencies.Output('table_figure_2012', 'figure'), 
    dash.dependencies.Output('table_figure_2017', 'figure')],
    dash.dependencies.Input('map_dropdown', 'value'))
def update_table(value):
    """
    Updates the Table based upon the desired quantity to sort on, drops all other columns
    - rearranges table so that sorted table goes 3rd (after State, code)

    Args:
        value (string): String describing the metric to be plotted

    Returns:
        table_figure_2012 (px.Figure): 2012 table to be displayed on the Dash app
        table_figure_2017 (px.Figure): 2017 table to be displayed on the Dash app
    """
    ### Create Data Frame for 2012
    data_2012 = data[data['Year'] == '2012']
    data_2012 = data_2012.reset_index()
    data_2012 = data_2012.drop(columns=['Year'])
    # Shift code and value columns
    code_col = data_2012.pop('code')
    data_2012.insert(1, 'code', code_col)
    value_col = data_2012.pop(value)
    data_2012.insert(2, value, value_col)
    # Drop all other columns
    data_2012 = data_2012.loc[:, ['State', 'code', value]]
    data_2012 = data_2012.sort_values(by=[value], ascending=False)
    data_2012[value] = data_2012[value].round(4)

    ### Create 2012 Table
    fig_2012 = go.Figure()
    fig_2012.add_table(cells=dict(
                            values=[data_2012[col].tolist() for col in ['State', 'code', value]]
                        ), 
                        header=dict(
                            values=['State', 'State Code', titles_Dict[value] + ' in 2012']
                        ),
                        columnwidth=[0.23, 0.12, 0.65]
                 )
    fig_2012.update_layout(margin=dict(r=10, l=10, t=10, b=10),
                            paper_bgcolor="ghostwhite")

    ### Create Data Frame for 2017
    data_2017 = data[data['Year'] == '2017']
    data_2017 = data_2017.reset_index()
    data_2017 = data_2017.drop(columns=['Year'])
    # Shift code and value columns
    code_col = data_2017.pop('code')
    data_2017.insert(1, 'code', code_col)
    value_col = data_2017.pop(value)
    data_2017.insert(2, value, value_col)
    # Drop all other columns
    data_2017 = data_2017.loc[:, ['State', 'code', value]]
    data_2017 = data_2017.sort_values(by=[value], ascending=False)
    data_2017[value] = data_2017[value].round(4)

    ### Create 2017 Table
    fig_2017 = go.Figure()
    fig_2017.add_table(cells=dict(
                            values=[data_2017[col].tolist() for col in ['State', 'code', value]]
                        ), 
                        header=dict(
                            values=['State', 'State Code', titles_Dict[value] + ' in 2017']
                        ),
                        columnwidth=[0.23, 0.12, 0.65]
                )
    fig_2017.update_layout(margin=dict(r=10, l=10, t=10, b=10),
                            paper_bgcolor="ghostwhite")

    return fig_2012, fig_2017

###### END DASH APPLICATION ######


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
