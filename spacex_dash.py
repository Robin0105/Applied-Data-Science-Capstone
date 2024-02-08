# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children = [html.H1('SpaceX Launch Records Dashboard',
                                        style = {'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                  dcc.Dropdown(id = 'site-dropdown',
                                  options = [
                                      {'label': 'All Sites', 'value': 'ALL'},
                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                  ],
                                  placeholder = 'Select a Launch Site Here',
                                  value = 'ALL',
                                  searchable = True
                                  ),
                                  html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                  html.Div(dcc.Graph(id = 'success-pie-chart')),
                                  html.Br(),

                                  html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                  dcc.RangeSlider(id = 'payload-slider',
                                                  min = 0, max = 10000, step = 1000,
                                                  marks = {0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                  value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                  html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
                                 ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdown', component_property = 'value'))
def get_pie_chart(launch_site):
    filtered_df = spacex_df
    if launch_site == 'ALL':
        values = spacex_df.groupby('Launch Site')['class'].mean()
        labels = spacex_df.groupby('Launch Site')['Launch Site'].first()
        title = 'Total Success Launches for All Sites'

    else:
        launch_site_df = spacex_df[spacex_df['Launch Site'] == launch_site]
        success_count = launch_site_df[launch_site_df['class'] == 1]['class'].count()
        failed_count = launch_site_df[launch_site_df['class'] == 0]['class'].count()
        labels = ['Success', 'Failure']
        values = [success_count, failed_count]
        title = f'Success and Failure Counts for {launch_site}'

    fig = px.pie(names = labels, values = values, title = title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
              [Input(component_id = 'site-dropdown', component_property = 'value'),
               Input(component_id = 'payload-slider',component_property = 'value')])
def get_payload_chart(launch_site, payload_mass):
    if launch_site == 'ALL':
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], 
                x = "Payload Mass (kg)",
                y = "class",
                color = "Booster Version Category",
                hover_data = ['Launch Site'],
                title = 'Correlation Between Payload and Success for All Sites')
    else:
        df = spacex_df[spacex_df['Launch Site']==str(launch_site)]
        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], 
                x = "Payload Mass (kg)",
                y = "class",
                color = "Booster Version Category",
                hover_data = ['Launch Site'],
                title = 'Correlation Between Payload and Success for Site {}'.format(launch_site))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
