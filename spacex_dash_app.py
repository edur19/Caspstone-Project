# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Extract unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown for Launch Site Selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}  # Default "ALL" option
        ] + [{'label': site, 'value': site} for site in launch_sites],  # Dynamically add sites
        value='ALL',  # Default selected value
        placeholder="Select a Launch Site here",
        searchable=True  # Allow search in dropdown
    ),
    html.Br(),

    # TASK 2: Pie chart to show successful launches count
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: f"{i}" for i in range(int(min_payload), int(max_payload) + 1, 5000)},
        value=[min_payload, max_payload]  # Default slider range
    ),
    html.Br(),

    # TASK 4: Scatter chart for payload vs. launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Total successful launches for all sites
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        # Success vs. Failure count for a specific site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Success vs. Failure for {selected_site}')
    return fig

# TASK 4: Add callback for scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if selected_site == 'ALL':
        # Show all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Launch Site',
                         title='Correlation between Payload and Success for All Sites')
    else:
        # Show specific site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         title=f'Correlation between Payload and Success for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8080)  
