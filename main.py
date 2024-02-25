import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

df = pd.read_csv("./historical_automobile_sales.csv")

df.head()
print(df)

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years
year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div(children=[html.H1('Automobile Sales Statistics Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                        'font-size': 24}), html.Div([html.Label("Select Statistics:"), dcc.Dropdown(
                                        id='dropdown-statistics',
                                        options=[{'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
                value='Select Statistics',
                placeholder='Select a report type')]), html.Div(dcc.Dropdown(
                id='select-year',
                options=[{'label': i, 'value': i} for i in year_list],
                value='Select Year')),
            html.Div(children=[html.H1('output-container', className='chart-grid',
                style={'display': 'flex'})])
    ])


# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year',
                                                                          component_property='value')])
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = df[df['Recession'] == 1]

        # TASK 2.5: Create and display graphs for Recession Report Statistics

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise)

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        r_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                            x='Year',
                            y='Automobile_Sales',
                            title="Average Automobile Sales fluctuation over Recession Period"))

        # Plot 2 Calculate the average number of vehicles sold by vehicle type

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        r_chart2 = dcc.Graph(figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Automobile Sales by Vehicle Type during Recession Period"))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        r_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Total Expenditures by Vehicle Type during Recession Period"))

        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_rate = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        r_chart4 = dcc.Graph(
            figure=px.bar(unemp_rate,
                          x='unemployment_rate',
                          y='Automobile_Sales',
                          title="Effects of Unemployment Rate on Automobile Sales by Vehicle Type during Recession "))

        return [
            html.Div(className='chart-item', children=[html.Div(children=r_chart1), html.Div(children=r_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=r_chart3), html.Div(children=r_chart4)],
                     style={'display': 'flex'})
        ]

    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # Yearly Statistic Report Plots
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == input_year]

        # TASK 2.5: Creating Graphs Yearly data

        # plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = df.groupby('Year')['Automobile_Sales'].sum().reset_index()
        y_chart1 = dcc.Graph(figure=px.line(yas,
                x='Year',
                y='Automobile_Sales',
                title='Automobile Sales for the Year'))

        # Plot 2 Total Monthly Automobile sales using line chart.
        df['Month'] = pd.to_datetime(df['Month'])
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           title='Total Automobile Sales by Month'))

        # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                            x='Year',
                            y='Automobile_Sales',
                            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle Type')['Advertising_Expenditure'].sum().reset_index()
        y_chart4 = dcc.Graph(figure=px.pie(exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertising Expenditure by Vehicle Type'))

        # TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            dcc.Graph(figure=y_chart1),
            dcc.Graph(figure=y_chart2),
            dcc.Graph(figure=y_chart3),
            dcc.Graph(figure=y_chart4)
        ]

# Run the Dash app


if __name__ == '__main__':
    app.run_server(debug=True)


y_chart1.show()
