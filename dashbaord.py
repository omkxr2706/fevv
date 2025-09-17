import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Sample data
modes = ['Eco Mode', 'Normal Mode', 'Sport Mode']
hours = [4.0, 3.5, 2.0]
soc = [25, 40, 35]

def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Mode", "Hours Used", "SOC Used (%)"],
                    fill_color='red', font=dict(color='white', size=16)),
        cells=dict(values=[modes, hours, soc],
                   fill_color='white', font=dict(color='red', size=14))
    )])
    fig.update_layout(margin=dict(t=10, b=10))
    return fig

app.layout = html.Div([
    # Sidebar toggle button
    html.Button('☰ Menu', id='btn_sidebar', n_clicks=0, style={'position': 'fixed', 'top': '15px', 'left': '15px', 
                                                               'background-color': 'red', 'color': 'white', 'border': 'none',
                                                               'padding': '10px 15px', 'zIndex': 9999}),

    # Sidebar container
    html.Div([
        html.Div([
            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/8/8f/FEV_Logo.jpg", 
                     style={'height':'60px', 'margin-bottom':'10px'}),
            html.H2("FEV", style={'color':'red', 'margin': '0'}),
        ], style={'text-align':'center', 'padding':'20px'}),

        html.Div([
            html.Div("USERNAME", style={'color':'red', 'font-weight': 'bold', 'margin-bottom': '5px'}),
            html.Div("USERNAME@FEV.com", style={'color':'darkred', 'font-size': '12px'}),
        ], style={'padding': '0 15px', 'margin-bottom': '20px'}),

        html.Nav([
            html.A("Eco Mode", href="#", style={'display':'block', 'color':'red', 'padding':'10px 15px', 'text-decoration':'none'}),
            html.A("Normal Mode", href="#", style={'display':'block', 'color':'red', 'padding':'10px 15px', 'text-decoration':'none'}),
            html.A("Sport Mode", href="#", style={'display':'block', 'color':'red', 'padding':'10px 15px', 'text-decoration':'none'}),
        ]),
    ], id='sidebar', style={
        'position': 'fixed',
        'width': '220px',
        'height':'100%',
        'background-color':'white',
        'box-shadow': '2px 0 5px rgba(0,0,0,0.1)',
        'padding-top': '20px',
        'overflow': 'auto',
        'zIndex': 999,
        'left': '0'
    }),

    # Main content area
    html.Div([
        html.H1("EV Profile Dashboard", style={'color':'red', 'text-align': 'center', 'margin-bottom':'30px'}),
        dcc.Graph(figure=create_table()),
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
        # Hide sidebar
        sidebar_style['left'] = '-220px'
        main_style['margin-left'] = '30px'
    else:
        # Show sidebar
        sidebar_style['left'] = '0'
        main_style['margin-left'] = '240px'
    return sidebar_style, main_style


if __name__ == '__main__':
    app.run(debug=True)
