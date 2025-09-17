import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import pandas as pd


# Load your large dataset CSV file
def load_and_process_data():
    df = pd.read_csv('ev_mode_usage_dataset.csv')
    df['soc_used'] = 100 - df['soc_percent']
    summary = df.groupby('mode').agg(
        hours_used=('timestamp_ms', lambda x: (x.max() - x.min()) / (1000 * 60 * 60)),
        avg_soc_used=('soc_used', 'mean')
    ).reset_index()
    return summary


def create_table(summary):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Mode", "Hours Used", "Average SOC Used (%)"],
            fill_color='red', font=dict(color='white', size=16)),
        cells=dict(
            values=[
                summary['mode'],
                summary['hours_used'].round(4),
                summary['avg_soc_used'].round(4)
            ],
            fill_color='white', font=dict(color='red', size=14))
    )])
    fig.update_layout(margin=dict(t=10, b=10))
    return fig


app = dash.Dash(__name__)

# Load initial data once at startup
summary_data = load_and_process_data()

app.layout = html.Div([
    html.Button('☰ Menu', id='btn_sidebar', n_clicks=0, style={
        'position': 'fixed', 'top': '15px', 'left': '15px',
        'background-color': 'red', 'color': 'white', 'border': 'none',
        'padding': '10px 15px', 'zIndex': 9999}),
    html.Div([
        html.Div([
            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/8/8f/FEV_Logo.jpg", style={'height':'60px', 'margin-bottom':'10px'}),
            html.H2("FEV", style={'color':'red', 'margin': '0'}),
        ], style={'text-align':'center', 'padding':'20px'}),
        html.Div([
            html.Div("USERNAME", style={'color':'red', 'font-weight': 'bold', 'margin-bottom': '5px'}),
            html.Div("USERNAME@FEV.com", style={'color':'darkred', 'font-size': '12px'}),
        ], style={'padding': '0 15px', 'margin-bottom': '20px'}),
        html.Nav([
            html.A("Economy", href="#", style={'display':'block', 'color':'red', 'padding':'10px 15px', 'text-decoration':'none'}),
            html.A("Normal", href="#", style={'display':'block', 'color':'red', 'padding':'10px 15px', 'text-decoration':'none'}),
            html.A("Sports", href="#", style={'display':'block', 'color':'red', 'padding':'10px 15px', 'text-decoration':'none'}),
        ]),
    ], id='sidebar', style={
        'position':'fixed',
        'width':'220px',
        'height':'100%',
        'background-color':'white',
        'box-shadow': '2px 0 5px rgba(0,0,0,0.1)',
        'padding-top': '20px',
        'overflow': 'auto',
        'zIndex': 999,
        'left': '0'
    }),
    html.Div([
        html.H1("EV Profile Dashboard", style={'color':'red', 'text-align': 'center', 'margin-bottom':'30px'}),
        dcc.Graph(id='table-graph', figure=create_table(summary_data)),
    ], id='main_content', style={
        'margin-left': '240px',
        'padding': '20px',
        'transition': 'margin-left 0.3s ease'
    })
])


@app.callback(
    Output('sidebar', 'style'),
    Output('main_content', 'style'),
    Input('btn_sidebar', 'n_clicks'),
    State('sidebar', 'style'),
    State('main_content', 'style')
)
def toggle_sidebar(n_clicks, sidebar_style, main_style):
    if n_clicks % 2 == 1:
        sidebar_style['left'] = '-220px'
        main_style['margin-left'] = '30px'
    else:
        sidebar_style['left'] = '0'
        main_style['margin-left'] = '240px'
    return sidebar_style, main_style


if __name__ == '__main__':
    app.run(debug=True)
