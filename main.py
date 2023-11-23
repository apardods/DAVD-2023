import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from prophet import Prophet

import data_load
import ml_methods

X = data_load.load_X('Real GDP', 'CPI', 'Unemployment')
y = data_load.load_target_data('Natural Gas')
result_df = pd.DataFrame()
app = dash.Dash(__name__)
macro_variables = ['Real GDP', 'Real GDP per capita', 'Treasury Yield', 'Federal Funds Rate', 'CPI', 'Inflation', 'Retail Sales', 'Durables', 'Unemployment', 'Nonfarm Payroll']
commodities = ['Crude Oil WTI', 'Crude Oil Brent', 'Natural Gas', 'Copper', 'Aluminum', 'Wheat', 'Corn', 'Cotton', 'Sugar', 'Coffee', 'CMI']
regression_techniques = ['Linear Regression', 'Random Forest', 'SVM']

app.layout = html.Div([
    html.Div(
        children=[
            html.H1('Commodity Price Stress Testing Tool'),
            html.P('''To make the models, select the desired macro and target variables. 
                   You will then see plots for all the selected variables (and the correlations 
                   for explanatory variables).'''),
            html.P('''Then select a ML methodology, and you will see a 
                   conclusion of the model, trained with automatic hyperparameter optimization.'''),
            html.P('''You will also see a forecast for future values of the commodity price, powered
                   by Meta's Prophet Engine.'''),
        ],
        style={
            'textAlign': 'center',
            'marginBottom': 20,
        }
    ),
    html.Div([
    #topleft
    dcc.Store(id='X'),
    dcc.Store(id='y'),
    html.Div([
        html.H2('Macro Variables Analysis', style={'textAlign': 'center'}),
        dcc.Dropdown(id='macro-var-1', options=[{'label': var, 'value': var} for var in macro_variables],
                    value='Real GDP', clearable=False, style={'width': '200px', 'display': 'inline-block'}),
        dcc.Dropdown(id='macro-var-2', options=[{'label': var, 'value': var} for var in macro_variables],
                    value='CPI', clearable=False, style={'width': '200px', 'display': 'inline-block'}),
        dcc.Dropdown(id='macro-var-3', options=[{'label': var, 'value': var} for var in macro_variables],
                    value='Unemployment', clearable=False, style={'width': '200px', 'display': 'inline-block'}),
        dcc.Graph(id='macroeconomic-plots')
    ], style={'display': 'inline-block', 'width' : '60%', 'verticalAlign': 'top'}),

    #topright
    html.Div([
        html.H2('Regression Output Table', style={'textAlign': 'center'}),
        dcc.Dropdown(id='commodity-dropdown', options=[{'label': commodity, 'value': commodity} for commodity in commodities],
                     value='Natural Gas', clearable=False, style = {'width': '50%'}),
        dcc.Graph(id='commodity-plot')
    ], style={'display': 'inline-block', 'width': '40%', 'verticalAlign': 'top'}),

    #botleft
    html.Div([
        html.H2('Regression Output Table', style={'textAlign': 'center'}),
        dcc.Dropdown(id='regression-dropdown', options=[{'label': technique, 'value': technique} for technique in regression_techniques],
                     value='Linear Regression', clearable=False),
        dash.dash_table.DataTable(
            id='regression-table'
        )

    ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top'}),

    #botright
    html.Div([
        html.H2('Forecast Commodity Price W/ Prophet', style={'textAlign': 'center'}),
        dcc.Graph(id='forecast-plot')
    ], style={'display': 'inline-block', 'width': '70%', 'verticalAlign': 'top'})
    ])
])


@app.callback(
    [Output('macroeconomic-plots', 'figure'),
     Output('X', 'data')],
    [Input('macro-var-1', 'value'),
     Input('macro-var-2', 'value'),
     Input('macro-var-3', 'value')]
)
def update_macroeconomic_plots(selected_variable1, selected_variable2, selected_variable3):
    df1 = data_load.load_macro_data(selected_variable1)
    df2 = data_load.load_macro_data(selected_variable2)
    df3 = data_load.load_macro_data(selected_variable3)
    X = pd.concat([df1, df2, df3], axis=1).dropna()
    fig = make_subplots(rows=2, cols=2, subplot_titles=[selected_variable1, selected_variable2, selected_variable3, 'Correlation Heatmap'])
    fig.add_trace(go.Scatter(x=df1.index, y=df1[selected_variable1], mode='lines', name=selected_variable1), row=1, col=1)
    fig.add_trace(go.Scatter(x=df2.index, y=df2[selected_variable2], mode='lines', name=selected_variable2), row=1, col=2)
    fig.add_trace(go.Scatter(x=df3.index, y=df3[selected_variable3], mode='lines', name=selected_variable3), row=2, col=1)
    corr = X.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    corr_mask = corr.mask(mask)
    fig.add_trace(go.Heatmap(z=corr_mask,
                             x=corr_mask.columns.values,
                             y=corr_mask.columns.values,
                             colorscale='RdBu',
                             #colorbar=dict(title='Correlation'),
                             zmin=-1, zmax=1),
                  row=2, col=2)
    fig.update_layout(showlegend=False)
    return fig, X.to_dict('records')



@app.callback(
    [Output('commodity-plot', 'figure'),
     Output('y', 'data')],
    [Input('commodity-dropdown', 'value'),]
)
def update_commodity_plot(selected_commodity):
    y = data_load.load_target_data(selected_commodity)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y.index, y=y[selected_commodity], mode='lines', name=selected_commodity))
    fig.update_layout(xaxis_title='Date', yaxis_title='Price')
    return fig, y.to_dict('records')


@app.callback(
    Output('regression-table', 'data'),
    [Input('regression-dropdown', 'value'),
     Input('X','data'),
     Input('y', 'data')]
)
def update_regression_table(selected_regression, X, y):
    if (X is None) or (y is None):
        return None
    X = pd.DataFrame(X)
    y = pd.DataFrame(y)
    common_index = X.index.intersection(y.index)
    y_filtered = y.loc[common_index]
    if selected_regression == 'Linear Regression':
        return ml_methods.fit_linear_regression(y_filtered, X).to_dict('records')
    if selected_regression == 'Random Forest':
        return ml_methods.fit_random_forest(y_filtered, X).to_dict('records')
    if selected_regression == 'SVM':
        return ml_methods.fit_svm(y_filtered, X).to_dict('records')

@app.callback(
    Output('forecast-plot', 'figure'),
    [Input('y', 'data'),
     Input('commodity-dropdown', 'value')]
)
def update_forecast_plot(y, selected_commodity):
    y = pd.DataFrame(y)
    latest_quarter = pd.to_datetime('today').to_period('Q').end_time
    y.reset_index(inplace=True)
    y['ds'] = pd.date_range(end=latest_quarter, periods=len(y), freq='Q')
    y.rename(columns={ selected_commodity: 'y'}, inplace=True)
    y.drop(['index'], inplace=True, axis=1)
    model = Prophet()
    model.fit(y)
    periods = len(y)//5
    future = model.make_future_dataframe(periods=periods, freq='Q')
    forecast = model.predict(future)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y['ds'], y=y['y'], mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(x=forecast['ds'][len(y)-1:], y=forecast['yhat'][len(y)-1:], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'][len(y)-1:], y=forecast['yhat_upper'][len(y)-1:], fill=None, mode='lines', line_color='rgba(0,100,80,0.2)', name='Upper Bound'))
    fig.add_trace(go.Scatter(x=forecast['ds'][len(y)-1:], y=forecast['yhat_lower'][len(y)-1:], fill='tonexty', mode='lines', line_color='rgba(0,100,80,0.2)', name='Lower Bound'))
    fig.update_layout(xaxis_title='Date',
                      yaxis_title='Value')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)