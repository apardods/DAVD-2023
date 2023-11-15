import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

import data_load
import ml_methods

app = dash.Dash(__name__)
X = pd.DataFrame()
y = pd.Series()
selected_commodity = ""
result_df = pd.DataFrame()
macro_variables = ['Real GDP', 'Real GDP per capita', 'Treasury Yield', 'Federal Funds Rate', 'CPI', 'Inflation', 'Retail Sales', 'Durables', 'Unemployment', 'Nonfarm Payroll']
commodities = ['Crude Oil WTI', 'Crude Oil Brent', 'Natural Gas', 'Copper', 'Aluminum', 'Wheat', 'Corn', 'Cotton', 'Sugar', 'Coffee', 'CMI']
regression_techniques = ['Linear Regression', 'Random Forest', 'SVM']

app.layout = html.Div([
    #topleft
    html.Div([
        dcc.Dropdown(id='macro-var-1', options=[{'label': var, 'value': var} for var in macro_variables],
                     value='Variable 1', clearable=False),
        dcc.Dropdown(id='macro-var-2', options=[{'label': var, 'value': var} for var in macro_variables],
                     value='Variable 2', clearable=False),
        dcc.Dropdown(id='macro-var-3', options=[{'label': var, 'value': var} for var in macro_variables],
                     value='Variable 3', clearable=False),
        dcc.Graph(id='macroeconomic-plots')
    ], className='four columns'),

    #topright
    html.Div([
        dcc.Dropdown(id='commodity-dropdown', options=[{'label': commodity, 'value': commodity} for commodity in commodities],
                     value='Commodity 1', clearable=False),
        dcc.Graph(id='commodity-plot')
    ], className='four columns'),

    #botleft
    html.Div([
        dcc.Dropdown(id='regression-dropdown', options=[{'label': technique, 'value': technique} for technique in regression_techniques],
                     value='Regression 1', clearable=False),
        dash.dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in result_df.columns],
            data=result_df.to_dict('records'),
        )

    ], className='four columns'),

    #botright
    html.Div(id='bottom-right-content', className='four columns')
])

# Define callbacks (you need to implement these callbacks)
@app.callback(
    Output('macroeconomic-plots', 'figure'),
    [Input('macro-var-1', 'value'),
     Input('macro-var-2', 'value'),
     Input('macro-var-3', 'value')]
)
def update_macroeconomic_plots(selected_variable1, selected_variable2, selected_variable3):
    df1 = data_load.load_macro_data(selected_variable1)
    df2 = data_load.load_macro_data(selected_variable2)
    df3 = data_load.load_macro_data(selected_variable3)

    X = pd.concat([df1, df2, df3], axis=1)
    fig = make_subplots(rows=2, cols=2, subplot_titles=[selected_variable1, selected_variable2, selected_variable3, 'Correlation Heatmap'])
    fig.add_trace(go.Scatter(x=df1.index, y=df1['value'], mode='lines', name=selected_variable1), row=1, col=1)
    fig.add_trace(go.Scatter(x=df2.index, y=df2['value'], mode='lines', name=selected_variable2), row=1, col=2)
    fig.add_trace(go.Scatter(x=df3.index, y=df3['value'], mode='lines', name=selected_variable3), row=2, col=1)
    correlation_matrix = pd.concat([df1['value'], df2['value'], df3['value']], axis=1).corr()
    print(correlation_matrix)
    fig.add_trace(go.Heatmap(z=correlation_matrix.values,
                             x=correlation_matrix.columns,
                             y=correlation_matrix.columns,
                             colorscale='Viridis',
                             colorbar=dict(title='Correlation'),
                             zmin=-1, zmax=1),
                  row=2, col=2)
    fig.update_layout(title_text='Macro Variables Analysis', showlegend=False)
    return fig

@app.callback(
    Output('commodity-plot', 'figure'),
    [Input('commodity-dropdown', 'value')]
)
def update_commodity_plot(selected_commodity):
    y = data_load.load_target_data(selected_commodity)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y.index, y=y['value'], mode='lines', name=selected_commodity))
    fig.update_layout(title_text='Time Series Plot', xaxis_title='Date', yaxis_title='Price')
    return fig


@app.callback(
    Output('table', 'data'),
    [Input('regression-dropdown', 'value')]
)
def update_regression_table(selected_regression):
    if selected_regression == 'Linear Regression':
        return ml_methods.fit_linear_regression(y, X)
    if selected_regression == 'Random Forest':
        return ml_methods.fit_random_forest(y, X)
    if selected_regression == 'SVM':
        return ml_methods.fit_svm(y, X)



if __name__ == '__main__':
    app.run_server(debug=True)