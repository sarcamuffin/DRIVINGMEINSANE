import dash
from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
background_color = '#FFF3E0'  # light orange
text_color = '#333'  # Dark grey for text
plotly_colors = ['#FFB600', '#EB8C00', '#D04A02', '#DB536A', '#E0311E', '#000000']

# App layout
# Data for the table
data = [
    {"Chapitre": "Sécurité physique et environnementale", "Moyenne des scores": 3.38},
    {"Chapitre": "Organisation de la sécurité des SI", "Moyenne des scores": 3.04},
    {"Chapitre": "Contrôle d'accès", "Moyenne des scores": 3.33},
    {"Chapitre": "Gestion des incidents de cybersécurité", "Moyenne des scores": 2.98},
    {"Chapitre": "Relations avec les fournisseurs", "Moyenne des scores": 3.21},
    {"Chapitre": "Sécurité liée à l'exploitation", "Moyenne des scores": 3.36},
    {"Chapitre": "Sécurité des RH", "Moyenne des scores": 3.16},
    {"Chapitre": "Gestion des actifs Informationnels", "Moyenne des scores": 3.14},
    {"Chapitre": "Cryptographie", "Moyenne des scores": 3.00},
    {"Chapitre": "Acquisition, développement et maintenance des SI", "Moyenne des scores": 3.32},
    {"Chapitre": "Conformité", "Moyenne des scores": 3.17},
    {"Chapitre": "Sécurité des communications", "Moyenne des scores": 3.31},
    {"Chapitre": "Gestion de continuité d’activité", "Moyenne des scores": 3.00},
]#


# Initialize the Dash app (usually in a real app you would modify this to suit your actual app server)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define colors
#background_color = '#FFF3E0'  # light orange

# App layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Tableau de bord de maturité cyber en conformité avec les réglementations nationales",
                style={'textAlign': 'center', 'margin': '20px', 'color': text_color}),
        html.Div("Vous avez choisi : DNSSI", style={'margin': '10px 0px', 'color': text_color}),
        html.Div([
            "La Directive Nationale de la Sécurité des Systèmes d'Information (DNSSI) au Maroc est un cadre juridique crucial "
            "pour la protection des systèmes d'information des administrations et infrastructures vitales. "
            "Adoptée en 2014 et régulièrement mise à jour, elle vise à renforcer la cybersécurité face aux menaces croissantes, "
            "assurant ainsi un développement numérique sécurisé et responsable au niveau national."
        ], style={'margin': '10px 0px 20px 0px', 'color': text_color}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in data[0].keys()],
            data=data,
            style_cell={'textAlign': 'center', 'padding': '10px', 'fontFamily': 'Arial', 'fontSize': 14},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold',
                'color': 'black'
            },
            style_data={
                'backgroundColor': 'white',
                'color': 'black'
            },
            style_table={'margin': 'auto', 'width': '100%', 'borderRadius': '8px', 'boxShadow': '2px 2px 10px #ccc'},
            fill_width=True
        ),
        html.Button("Suivant", id='next-page-button', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
    ], fluid=True),
    html.Div(id='page-content')
], style={'fontFamily': 'Arial', 'padding': '20px', 'backgroundColor': background_color, 'width': '100%', 'height': '100vh'})


@app.callback(
    Output('page-content', 'children'),
    Input('next-page-button', 'n_clicks')
)
def display_page(n_clicks):
    if n_clicks > 0:
        # Here you would normally fetch or calculate the data needed for your plots
        df = pd.DataFrame(data)
        # Plotting
        fig_bar = px.bar(df, x='Chapitre', y='Moyenne des scores', title="Scores by Chapter", color_discrete_sequence=plotly_colors)
        fig_pie = px.pie(df, values='Moyenne des scores', names='Chapitre', title="Distribution of Scores", color_discrete_sequence=plotly_colors)
        # Assuming you have a heatmap-ready dataframe (usually requires preprocessing)
        # For demo purposes, using the same df for a heatmap (not typical)
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=df['Moyenne des scores'],
            x=df['Chapitre'],
            y=['Scores'],
            colorscale=plotly_colors
        ))

        return dbc.Container([
            dcc.Graph(figure=fig_bar),
            dcc.Graph(figure=fig_pie),
            dcc.Graph(figure=fig_heatmap)
        ], fluid=True)
    return ""

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8083)
