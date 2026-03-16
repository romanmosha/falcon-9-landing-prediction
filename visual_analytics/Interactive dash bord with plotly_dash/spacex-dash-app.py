# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Prepare dropdown options list
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + \
               [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1(child):  Dropdown child for list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites,
        value='ALL',  # default select value
        placeholder='Select a Launch Site',
        searchable=True
    ),

    #Task 2 child to add pie chart graph
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
    
    #Task 3 child to add ranger slider
    html.Br(),
    dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    marks={i: f'{i}' for i in range(0, 10001, 1000)},
    value=[min_payload, max_payload]
),

#Task 4 child to add scatter plot
html.Br(),
dcc.Graph(id='success-payload-scatter-chart'),
])

#Task 2 Add call back function to render success pie chart based on selected site drop dwon
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter for successful launches only
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        # Filter data for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(success_counts, names='class', values='count',
                     title=f'Success vs Failure for site {selected_site}')
    return fig
#TASK 3: Add a Range Slider to Select Payload
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    if selected_site == 'ALL':
        # Filter data by payload range only
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                                (spacex_df['Payload Mass (kg)'] <= high)]
    else:
        # Filter data by selected site and payload range
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= low) &
                                (spacex_df['Payload Mass (kg)'] <= high)]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Outcome for Selected Site(s)',
        labels={'class': 'Launch Outcome (0=Failure, 1=Success)'}
    )
    return fig

if __name__ == '__main__':
    #app.run()
    #app.run_server(debug=True)
    app.run(debug=True)