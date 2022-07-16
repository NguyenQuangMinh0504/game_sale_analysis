import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

data = pd.read_csv("data/vgsales.csv")
data.drop(data[data.Year >= 2017].index, axis=0, inplace=True)

colors_dict = {"Global_Sales": "#1f77b4", "NA_Sales": "#ff7f0e",
               "EU_Sales": "#d62728", "JP_Sales": "#9467bd", "Other_Sales": "#8c546b"}
# --------------------------------------------------------------------------------#
# Plot Sales by region
df = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
df = pd.DataFrame(df, columns=['Sales']).sort_values('Sales', ascending=False)
df.reset_index(inplace=True)
region_sales_fig = px.bar(df, x="Sales", y="index", orientation='h',
                          text_auto=True, template="plotly_dark", title=None,
                          color="index", color_discrete_map=colors_dict)
region_sales_fig.update_layout(clickmode='event+select')

# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Total Sales by genre
genre_total_df = data.groupby('Genre', as_index=False).sum().sort_values('Global_Sales', ascending=True)
# --------------------------------------------------------------------------------#


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Video game sales analysis",
                        className="text-center text-primary mb-4"),
                width=12)
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                         options=[{'label': x, 'value': x} for x in [1, 2, 3]]),
            # Sales by region figure
            dcc.Graph(id='region_sales_fig', figure=region_sales_fig)
        ], width={'size': 5, 'offset': 1}),

        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['PPTX', 'FFNM'],
                         options=[{'label': x, 'value': x} for x in [1, 2, 3]]),
            # Sales by Genre figure
            dcc.Graph(id='genre_sales_fig', figure={})
        ], width={'size': 5, 'offset': 0})

    ]),  # justify = 'start,end,center, between, around'

    dbc.Row([

        dbc.Col([
            html.P('Stock : ',
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label': x, 'value': x} for x in [1, 2, 3]],
                          labelClassName='mr-3 text-success'),
            # Sales Over Time Figure
            dcc.Graph(id='sales_over_time_fig', figure={})
        ], width={'size': 10, 'offset': 1})

    ])
], fluid=True)


# Update sales by genre figure when user selects region
@app.callback(
    Output('genre_sales_fig', 'figure'),
    Input('region_sales_fig', 'selectedData')
)
def update_genre_graph(selectedData):
    if (selectedData != None and selectedData["points"][0]['label'] != "Global_Sales"):
        label = selectedData["points"][0]['y']
        fig = px.bar(genre_total_df, x=label, y="Genre", orientation='h',
                     text_auto=True, template="plotly_dark", title=None,
                     barmode='stack', color_discrete_sequence=[colors_dict[label]])
    else:
        label = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
        fig = px.bar(genre_total_df, x=label, y="Genre", orientation='h',
                     text_auto=True, template="plotly_dark", title=None,
                     barmode='stack', color_discrete_map=colors_dict)
    fig.update_layout(clickmode='event+select')

    return (fig)


# Update sales over time figure when user selects region and genre
@app.callback(
    Output('sales_over_time_fig', 'figure'),
    [Input('region_sales_fig', 'selectedData'),
     Input('genre_sales_fig', 'selectedData')]
)
def update_time_graph(regionSelectedData, genreSelectedData):
    region = regionSelectedData["points"][0]['y'] if regionSelectedData != None else "Global_Sales"
    genre = genreSelectedData["points"][0]['y'] if genreSelectedData != None else "All"

    if (genre != "All"):
        genre_df = data[data["Genre"] == genre]
        genre_df.groupby('Year').sum()
        fig = px.line(pd.DataFrame(genre_df.groupby('Year', as_index=False).sum()), x="Year", y=region,
                      title=genre + " sales in " + region, markers=True, template="plotly_dark",
                      color_discrete_sequence=[colors_dict[region]])
    else:
        genre_df = pd.DataFrame(data.groupby('Year', as_index=False).sum())
        fig = px.line(genre_df, x="Year", y=region,
                      title=genre + " sales in " + region, markers=True, template="plotly_dark",
                      color_discrete_sequence=[colors_dict['Global_Sales']])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)