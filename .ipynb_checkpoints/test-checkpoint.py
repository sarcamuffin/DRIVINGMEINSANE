import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from dash import dash_table

# Custom color scheme
colors = {
    'background': '#F9F9F9',
    'text': '#007BFF',
    'plotly': ['#007BFF', '#FF4136', '#2ECC40', '#FF851B', '#7FDBFF', '#B10DC9'],
    'card_background': '#FFFFFF'
}

# Reading and processing data
try:
    df = pd.read_csv('data.csv', delimiter=';')
    mapping_df = pd.read_excel('Mapping_noms_variables_sphinx.xlsx')
    column_mapping = dict(zip(mapping_df['Anciens Noms'], mapping_df['Nouveaux Noms']))
    df.rename(columns=column_mapping, inplace=True)
    client_name = 'emi'
    df_emi = df[df['Clien_Name'] == client_name]
    excluded_columns = ["Clien_Name", "Secteur", "axe-reglement", "reglement", "CLE",
                        "DATE_SAISIE", "DATE_ENREG", "DATE_MODIF", "TEMPS_SAISIE", "ORIGINE_SAISIE",
                        "LANG_SAISIE", "APPAREIL_SAISIE", "PROGRESSION", "DERNIERE_QUESTION_SAISIE"]
    included_columns = [col for col in df_emi.columns if col not in excluded_columns]
    themes = set(col.split(' -')[0] for col in included_columns if '-' in col)
    for theme in themes:
        theme_cols = [col for col in included_columns if col.startswith(theme)]
        df[theme + ' Moyenne'] = df[theme_cols].mean(axis=1)
    data_for_plot = df[[theme + ' Moyenne' for theme in themes]].mean().reset_index()
    data_for_plot.columns = ['Theme', 'Moyenne']
except Exception as e:
    print(f"Error preparing data: {e}")

# Visualization functions
def generate_graph(figure, title):
    return dcc.Graph(
        figure=figure.update_layout(
            plot_bgcolor=colors['card_background'],
            paper_bgcolor=colors['card_background'],
            title=title,
            title_font_color=colors['text'],
            font_color=colors['text']
        )
    )

# Creating visualizations
fig_bar = px.bar(data_for_plot, x='Theme', y='Moyenne', text_auto=True)
fig_scatter = px.scatter(data_for_plot, x='Theme', y='Moyenne', color='Moyenne', size='Moyenne')
fig_box = px.box(data_for_plot, y='Moyenne', x='Theme')
fig_hist = px.histogram(data_for_plot, x='Moyenne', nbins=20)
fig_heatmap = px.imshow(df[[theme + ' Moyenne' for theme in themes]].corr())
fig_radar = px.line_polar(data_for_plot, r='Moyenne', theta='Theme', line_close=True)

# App layout with cards
app = dash.Dash(__name__)
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Dashboard avec Graphiques', style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(className='row', children=[
        html.Div(className='four columns', children=[
            html.Div(style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '2px 2px 10px #aaa'}, children=[
                generate_graph(fig_bar, 'Moyenne de Maturité par Thème')
            ]),
        ]),
        html.Div(className='four columns', children=[
            html.Div(style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '2px 2px 10px #aaa'}, children=[
                generate_graph(fig_scatter, 'Scatter Plot de Maturité par Thème')
            ]),
        ]),
        html.Div(className='four columns', children=[
            html.Div(style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '2px 2px 10px #aaa'}, children=[
                generate_graph(fig_box, 'Box Plot de Maturité par Thème')
            ]),
        ]),
    ]),
    html.Div(className='row', children=[
        html.Div(className='four columns', children=[
            html.Div(style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '2px 2px 10px #aaa'}, children=[
                generate_graph(fig_hist, 'Histogramme de Maturité')
            ]),
        ]),
        html.Div(className='four columns', children=[
            html.Div(style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '2px 2px 10px #aaa'}, children=[
                generate_graph(fig_heatmap, 'Heatmap de Corrélation entre Thèmes')
            ]),
        ]),
        html.Div(className='four columns', children=[
            html.Div(style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '15px', 'boxShadow': '2px 2px 10px #aaa'}, children=[
                generate_graph(fig_radar, 'Radar Chart de Maturité par Thème')
            ]),
        ]),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
