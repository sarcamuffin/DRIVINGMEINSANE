import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

#colors = {
   # 'background': '#ffffff',
    #'text': '#000000',
    #'plotly': ['#FFB600', '#EB8C00', '#D04A02', '#DB536A', '#E0311E', '#000000']
#}

# Reading data files
try:
    df = pd.read_csv('data.csv', delimiter=';')
    mapping_df = pd.read_excel('Mapping_noms_variables_sphinx.xlsx')
except Exception as e:
    print(f"Error reading files: {e}")

# Creating mapping dictionary and renaming columns
try:
    column_mapping = dict(zip(mapping_df['Anciens Noms'], mapping_df['Nouveaux Noms']))
    df.rename(columns=column_mapping, inplace=True)
except Exception as e:
    print(f"Error mapping columns: {e}")

# Filtering data for a specific client
try:
    client_name = 'emi'
    df_emi = df[df['Clien_Name'] == client_name]
except Exception as e:
    print(f"Error filtering data for client '{client_name}': {e}")

# Defining columns to exclude and include
excluded_columns = [
    "Clien_Name", "Secteur", "axe-reglement", "reglement", "CLE",
    "DATE_SAISIE", "DATE_ENREG", "DATE_MODIF", "TEMPS_SAISIE", "ORIGINE_SAISIE",
    "LANG_SAISIE", "APPAREIL_SAISIE", "PROGRESSION", "DERNIERE_QUESTION_SAISIE"
]
included_columns = [col for col in df_emi.columns if col not in excluded_columns]

# Calculating average scores for themes
themes = set(col.split(' -')[0] for col in included_columns if '-' in col)
try:
    for theme in themes:
        theme_cols = [col for col in included_columns if col.startswith(theme)]
        if theme_cols:
            df[theme + ' Moyenne'] = df[theme_cols].mean(axis=1)
except Exception as e:
    print(f"Error calculating theme averages: {e}")

# Preparing data for plots
try:
    data_for_plot = df[[theme + ' Moyenne' for theme in themes]].mean().reset_index()
    data_for_plot.columns = ['Theme', 'Moyenne']
except Exception as e:
    print(f"Error preparing data for plots: {e}")

app = dash.Dash(__name__)

# Colors and style settings
colors = {
    'background': '#ffffff',
    'text': '#000000',
    'plotly': ['#FFB600', '#EB8C00', '#D04A02', '#DB536A', '#E0311E', '#000000']
}

# Bar chart for theme averages
fig_bar = px.bar(data_for_plot, x='Theme', y='Moyenne', title='Average Scores per Theme',
                 color='Moyenne', range_y=[0, 5] ,color_continuous_scale=px.colors.sequential.Viridis)

# Assuming you have a date column 'Date' in df for line chart
# fig_line = px.line(df, x='Date', y=[theme + ' Moyenne' for theme in themes], title='Trend Over Time')

# Scatter plot example, assuming you have at least two themes to compare
fig_scatter = px.scatter(df, x=themes.pop() + ' Moyenne', y=themes.pop() + ' Moyenne', title='Theme Comparison')

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Data Visualization with Dash and Plotly',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='bar-graph',
        figure=fig_bar
    ),

    # Uncomment these when the data and plots are correctly configured
    # dcc.Graph(
    #     id='line-graph',
    #     figure=fig_line
    # ),
    
    dcc.Graph(
         id='scatter-graph',
         figure=fig_scatter
     )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
