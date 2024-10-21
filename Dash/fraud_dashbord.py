import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Fraud Detection Dashboard"),
    dcc.Interval(id='interval-component', interval=20000, n_intervals=0),
    
    # Summary Boxes
    html.Div([
        html.Div(id="total-transactions", className="summary-box"),
        html.Div(id="fraud-cases", className="summary-box"),
        html.Div(id="fraud-percentage", className="summary-box"),
    ], className="summary-box-container"),

    # Fraud trend over time
    dcc.Graph(id="fraud-trend"),

    # Fraud geography
    dcc.Graph(id="fraud-geo"),

    # # Fraud by device
    # dcc.Graph(id="fraud-device"),

    # # Fraud by browser
    # dcc.Graph(id="fraud-browser")
])

# Callback to update summary stats
@app.callback(
    [Output('total-transactions', 'children'),
     Output('fraud-cases', 'children'),
     Output('fraud-percentage', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_summary_boxes(n):
    response = requests.get("http://127.0.0.1:5000/summary").json()
    total_transactions = f"Total Transactions: {response['total_transactions']}"
    fraud_cases = f"Fraud Cases: {response['fraud_cases']}"
    fraud_percentage = f"Fraud Percentage: {response['fraud_percentage']:.2f}%"
    
    return total_transactions, fraud_cases, fraud_percentage

# Callback to update fraud trend graph
@app.callback(
    Output('fraud-trend', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_fraud_trend(n):
    response = requests.get("http://127.0.0.1:5000/fraud_trends").json()
    fraud_trend_df = pd.DataFrame(response)
    
    fig = px.line(fraud_trend_df, x='purchase_time', y='class', title="Fraud Cases Over Time")
    return fig

# Callback to update fraud geography graph
@app.callback(
    Output('fraud-geo', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_fraud_geo(n):
    response = requests.get("http://127.0.0.1:5000/fraud_geography").json()
    fraud_geo_df = pd.DataFrame(response)
    
    fig = px.choropleth(fraud_geo_df, locations="country", color="class",
                        locationmode='country names', title="Fraud Cases by Country")
    return fig

# Callback to update fraud by device
# @app.callback(
#     Output('fraud-device', 'figure'),
#     [Input('interval-component', 'n_intervals')]
# )
# def update_fraud_device(n):
#     response = requests.get("http://127.0.0.1:5000/fraud_device_browser").json()
#     fraud_device_df = pd.DataFrame(response)
    
#     fig = px.bar(fraud_device_df, x='device_id', y='class', title="Fraud Cases by Device")
#     fig.update_traces(marker_color='orange')
    
#     return fig

# Callback to update fraud by browser
# @app.callback(
#     Output('fraud-browser', 'figure'),
#     [Input('interval-component', 'n_intervals')]
# )
# def update_fraud_browser(n):
#     response = requests.get("http://127.0.0.1:5000/fraud_device_browser").json()
#     fraud_browser_df = pd.DataFrame(response['fraud_browser'])
    
#     fig_browser = px.bar(fraud_browser_df, x='browser', y='class', title="Fraud Cases by Browser")
#     fig_browser.update_traces(marker_color='blue')
    
#     return fig_browser

if __name__ == '__main__':
    app.run_server(debug=True)
