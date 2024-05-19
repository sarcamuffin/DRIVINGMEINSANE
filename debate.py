import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from dash import dash_table

# Custom color scheme
colors = {
    'background': '#F9F9F9',
    'text': '#D04A02',  # PWC Dark Orange
    'card_background': '#FFFFFF',
    'plotly': ['#EB8C00', '#D04A02', '#DB536A', '#E0301E', '#000000']
}

# Reading and processing data
try:
    df = pd.read_csv('data.csv', delimiter=';')
    mapping_df = pd.read_excel('Mapping_noms_variables_sphinx.xlsx')
    column_mapping = dict(zip(mapping_df['Anciens Noms'], mapping_df['Nouveaux Noms']))
    df.rename(columns=column_mapping, inplace=True)
    client_name = 'client AM'
    df_emi = df[df['Clien_Name'] == client_name]

    excluded_columns = ["Clien_Name", "Secteur", "axe-reglement", "reglement", "CLE",
                        "DATE_SAISIE", "DATE_ENREG", "DATE_MODIF", "TEMPS_SAISIE", "ORIGINE_SAISIE",
                        "LANG_SAISIE", "APPAREIL_SAISIE", "PROGRESSION", "DERNIERE_QUESTION_SAISIE"]
    included_columns = [col for col in df_emi.columns if col not in excluded_columns]
    themes = set(col.split(' -')[0] for col in included_columns if '-' in col)
    for theme in themes:
        theme_cols = [col for col in included_columns if col.startswith(theme)]
        df_emi[theme + ' Moyenne'] = df_emi[theme_cols].mean(axis=1)
    data_for_plot = df_emi[[theme + ' Moyenne' for theme in themes]].mean().reset_index()
    data_for_plot.columns = ['Theme', 'Moyenne']
except Exception as e:
    print(f"Error preparing data: {e}")

# Visualization functions
def generate_graph(figure, title):
    return html.Div(className='card', children=[
        html.H2(title),
        dcc.Graph(
            figure=figure.update_layout(
                plot_bgcolor=colors['card_background'],
                paper_bgcolor=colors['card_background'],
                title=title,
                title_font_color=colors['text'],
                font_color=colors['text']
            )
        )
    ])

# Creating visualizations with custom colors
fig_bar = px.bar(data_for_plot, x='Theme', y='Moyenne', text_auto=True, color_discrete_sequence=colors['plotly'])
fig_scatter = px.scatter(data_for_plot, x='Theme', y='Moyenne', color='Moyenne', size='Moyenne', color_continuous_scale=colors['plotly'])
fig_box = px.box(data_for_plot, y='Moyenne', x='Theme', color_discrete_sequence=colors['plotly'])
fig_hist = px.histogram(data_for_plot, x='Moyenne', nbins=20, color_discrete_sequence=colors['plotly'])
fig_heatmap = px.imshow(df_emi[[theme + ' Moyenne' for theme in themes]].corr(), color_continuous_scale=colors['plotly'])
fig_radar = px.line_polar(data_for_plot, r='Moyenne', theta='Theme', line_close=True, color_discrete_sequence=colors['plotly'])

# Navigation bar
nav_bar = html.Div(className='nav-bar', children=[
    dcc.Link('Home', href='/', className='nav-link'),
    dcc.Link('Detailed Analysis', href='/details', className='nav-link'),
    dcc.Link('Comparative Analysis', href='/comparative', className='nav-link')
])

# Home page layout
home_layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    nav_bar,
    html.H1('DNSSI Compliance Dashboard', className='header'),
    html.P('This dashboard provides an interactive and animated view of DNSSI compliance scores for different chapters and sub-chapters. It allows you to compare and analyze the performance of various themes and chapters.'),
    html.Div(className='card table-container', children=[
        dash_table.DataTable(
            data=data_for_plot.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in data_for_plot.columns],
            style_table={'margin': '20px', 'width': '100%', 'overflowX': 'auto'},
            style_header={'backgroundColor': colors['card_background'], 'color': colors['text'], 'fontWeight': 'bold'},
            style_cell={'backgroundColor': colors['background'], 'color': colors['text']}
        )
    ]),
])

# Detailed page layout
detailed_layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    nav_bar,
    html.H1('Detailed Analysis', className='header'),
    html.Div(className='card-content', children=[
        generate_graph(fig_bar, 'Moyenne de Maturité par Thème'),
        generate_graph(fig_heatmap, 'Heatmap de Corrélation entre Thèmes'),
        generate_graph(fig_radar, 'Radar Chart de Maturité par Thème'),
        generate_graph(fig_box, 'Box Plot de Maturité par Thème'),
        generate_graph(fig_hist, 'Histogramme de Maturité'),
    ]),
])

# Comparative analysis layout
comparative_layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    nav_bar,
    html.H1('Comparative Analysis by Chapter', className='header'),
    html.Div(id='comparative-sections')
])

# App initialization
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "DNSSI Compliance Dashboard"
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to update the layout based on URL
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/details':
        return detailed_layout
    elif pathname == '/comparative':
        return comparative_layout
    else:
        return '404'

# Callback to generate comparative sections
@app.callback(
    dash.dependencies.Output('comparative-sections', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def generate_comparative_sections(pathname):
    if pathname == '/comparative':
        sections = []
        for theme in themes:
            theme_cols = [col for col in included_columns if col.startswith(theme)]
            theme_data = df_emi[theme_cols + [theme + ' Moyenne']]
            theme_plot = theme_data.mean().reset_index()
            theme_plot.columns = ['Sub-Theme', 'Moyenne']
            fig_theme_bar = px.bar(theme_plot, x='Sub-Theme', y='Moyenne', color='Moyenne', color_continuous_scale=colors['plotly'])
            fig_theme_pie = px.pie(theme_plot, values='Moyenne', names='Sub-Theme', color_discrete_sequence=colors['plotly'])
            
            section = html.Div(className='card', children=[
                html.H2(f'Chapter: {theme}', style={'color': colors['text']}),
                html.Div(className='card-content', children=[
                    html.Div(children=[
                        generate_graph(fig_theme_bar, f'{theme} Sub-Themes Bar Chart')
                    ]),
                    html.Div(children=[
                        generate_graph(fig_theme_pie, f'{theme} Sub-Themes Pie Chart')
                    ]),
                ]),
            ])
            sections.append(section)
        return sections

if __name__ == '__main__':
    app.run_server(debug=True, port=8087)
