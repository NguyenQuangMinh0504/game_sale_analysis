import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import ipywidgets as ipw
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots #import new library

data = pd.read_csv("data/vgsales.csv")
data.drop(data[data.Year >= 2017].index, axis=0, inplace=True)
data.drop(data.query("Name == 'Strongest Tokyo University Shogi DS'").index, axis=0, inplace=True)

colors_dict = {"Global_Sales": "#1f77b4", "NA_Sales": "#ff7f0e",
               "EU_Sales": "#d62728", "JP_Sales": "#9467bd", "Other_Sales": "#8c546b"}

# --------------------------------------------------------------------------------#
# Plot Sales by region
df = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
df = pd.DataFrame(df, columns=['Sales']).sort_values('Sales', ascending=False)
df.reset_index(inplace=True)
region_sales_fig = px.bar(df, x="Sales", y="index", orientation='h',
                          text_auto=True, title=None,
                          color="index", color_discrete_map=colors_dict)
region_sales_fig.update_traces(textposition="inside", cliponaxis=False, textangle=0)
region_sales_fig.update_layout(clickmode='event+select')

# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Total Sales by genre
genre_total_df = data.groupby('Genre', as_index=False).sum().sort_values('Global_Sales', ascending=True)
genre_sales_distribution_fig = px.pie(genre_total_df, values="Global_Sales", names="Genre",
                                      color="Genre", color_discrete_map=colors_dict)
# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Successive consoles timeline
nintendo_home_video_game_console = ["NES", "SNES", "N64", "GC", "Wii", "WiiU"]
sony_home_video_game_console = ["PS", "PS2", "PS3", "PS4"]
microsoft_home_video_game_console = ["XB", "X360", "XOne"]
sega_home_video_game_console = ["GEN", "SCD", "SAT", "DC"]
atari_home_video_game_console = ["2600"]
nec_home_video_game_console = ["TG16", "PCFX"]
other_home_video_game_console = ["NG", "3DO"]

console_dict = {"platform": [], "start": [], "finish": [], "manufacture": []}


def add_to_dict(name, platform):
    for i in platform:
        query = "Platform == '{}'".format(i)
        console_dict["platform"].append(i)
        console_dict["start"].append('{}-01-01'.format(
            int(data.query(query)["Year"].min())))
        console_dict["finish"].append('{}-12-31'.format(
            int(data.query(query)["Year"].max())))
        console_dict["manufacture"].append(name)


add_to_dict("Nintendo", nintendo_home_video_game_console)
add_to_dict("Sony", sony_home_video_game_console)
add_to_dict("Microsoft", microsoft_home_video_game_console)
add_to_dict("Sega", sega_home_video_game_console)
add_to_dict("Atari", atari_home_video_game_console)
add_to_dict("NEC", nec_home_video_game_console)
add_to_dict("Other", other_home_video_game_console)
console_df = pd.DataFrame(console_dict)

console_timeline_fig = px.timeline(
    console_df, x_start="start", x_end="finish", y="platform",
    color="manufacture", range_x=("1980-01-01", '2020-01-01'), text="platform",
    title="Home Video Game Console"
)
console_timeline_fig.update_yaxes(autorange="reversed")
# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Handheld console timeline

console_dict = {"platform": [], "start": [], "finish": [], "manufacture": []}

nintendo_handheld_game_console = ["GB", "GBA", "DS", "3DS"]
sony_handheld_game_console = ["PSP", "PSV"]
sega_handheld_game_console = ["GG"]
bandai_handheld_game_console = ["WS"]

add_to_dict("Nintendo", nintendo_handheld_game_console)
add_to_dict("Sony", sony_handheld_game_console)
add_to_dict("Sega", sega_handheld_game_console)
add_to_dict("Bandai", bandai_handheld_game_console)
console_df = pd.DataFrame(console_dict)

handheld_console_timeline_fig = px.timeline(
    console_df, x_start="start", x_end="finish", y="platform",
    color="manufacture", range_x=("1980-01-01", '2022-01-01'),
    title="HandHeld Video Game Console"
)
handheld_console_timeline_fig.update_yaxes(autorange="reversed")

# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Console manufacturer distribution over time
console_dict = {"manufacture": [], "number_of_game": []}


def add_to_dict(name, platform, query):
    console_dict["manufacture"].append(name)
    console_dict["number_of_game"].append(
        len(data.loc[data["Platform"].isin(platform)].query(query)
            )
    )


query1 = "Year < 1990"
query2 = "Year >= 1990 and Year < 2000"
query3 = "Year >= 2000 and Year < 2010"
query4 = "Year >= 2010"

add_to_dict("Nintendo", nintendo_home_video_game_console, query1)
add_to_dict("Sony", sony_home_video_game_console, query1)
add_to_dict("Microsoft", microsoft_home_video_game_console, query1)
add_to_dict("Sega", sega_home_video_game_console, query1)
add_to_dict("Atari", atari_home_video_game_console, query1)
add_to_dict("NEC", nec_home_video_game_console, query1)
add_to_dict("Other", other_home_video_game_console, query1)
console_df = pd.DataFrame(console_dict)
manufacturer_1980_fig = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7],
                               title="Number of games released on home Video Game Console 1980-1990")

console_dict = {"manufacture": [], "number_of_game": []}
add_to_dict("Nintendo", nintendo_home_video_game_console, query2)
add_to_dict("Sony", sony_home_video_game_console, query2)
add_to_dict("Microsoft", microsoft_home_video_game_console, query2)
add_to_dict("Sega", sega_home_video_game_console, query2)
add_to_dict("Atari", atari_home_video_game_console, query2)
add_to_dict("NEC", nec_home_video_game_console, query2)
add_to_dict("Other", other_home_video_game_console, query2)
console_df = pd.DataFrame(console_dict)
manufacturer_1990_fig = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7],
                               title="Number of games released on home Video Game Console 1990-2000")

console_dict = {"manufacture": [], "number_of_game": []}
add_to_dict("Nintendo", nintendo_home_video_game_console, query3)
add_to_dict("Sony", sony_home_video_game_console, query3)
add_to_dict("Microsoft", microsoft_home_video_game_console, query3)
add_to_dict("Sega", sega_home_video_game_console, query3)
add_to_dict("Atari", atari_home_video_game_console, query3)
add_to_dict("NEC", nec_home_video_game_console, query3)
add_to_dict("Other", other_home_video_game_console, query3)
console_df = pd.DataFrame(console_dict)
manufacturer_2000_fig = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7],
                               title="Number of games released on home Video Game Console 2000-2010")

console_dict = {"manufacture": [], "number_of_game": []}
add_to_dict("Nintendo", nintendo_home_video_game_console, query4)
add_to_dict("Sony", sony_home_video_game_console, query4)
add_to_dict("Microsoft", microsoft_home_video_game_console, query4)
add_to_dict("Sega", sega_home_video_game_console, query4)
add_to_dict("Atari", atari_home_video_game_console, query4)
add_to_dict("NEC", nec_home_video_game_console, query4)
add_to_dict("Other", other_home_video_game_console, query4)
console_df = pd.DataFrame(console_dict)
manufacturer_2010_fig = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7],
                               title="Number of games released on home Video Game Console from 2010")

# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Consoles Sales

consoles_manufacture_dict = {"NES": "Nintendo", "SNES": "Nintendo", "N64": "Nintendo",
                             "GC": "Nintendo", "Wii": "Nintendo", "WiiU": "Nintendo",
                             "PS": "Sony", "PS2": "Sony", "PS3": "Sony", "PS4": "Sony",
                             "XB": "Microsoft", "X360": "Microsoft", "XOne": "Microsoft",
                             "GEN": "Sega", "SCD": "Sega", "SAT": "Sega", "DC": "Sega",
                             "2600": "Atari",
                             "TG16": "NEC", "PCFX": "NEC",
                             "NG": "Other", "3DO": "Other",
                             "GB": "Nintendo", "GBA": "Nintendo", "DS": "Nintendo", "3DS": "Nintendo",
                             "PSP": "Sony", "PSV": "Sony",
                             "GG": "Sega",
                             "WS": "Bandai",
                             "PC": "Other"}

consoles_sales_df = data.groupby('Platform', as_index=False)['Global_Sales'].sum()
consoles_sales_df['Manufacture'] = None
for i in consoles_sales_df.index:
    consoles_sales_df.loc[i, "Manufacture"] = consoles_manufacture_dict[consoles_sales_df.iloc[i, 0]]

consoles_sales_fig = px.histogram(consoles_sales_df, x="Platform", y="Global_Sales", color="Manufacture")
# --------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------#
# Publisher Distribution
publishers_df = data.groupby('Publisher', as_index=False).sum().sort_values("Global_Sales", ascending=False)
publishers = publishers_df.head(15).Publisher.unique()
indices = []
for p in publishers:
    temp_df = data[data.Publisher == p].sort_values("Global_Sales", ascending=False)
    for i in temp_df.head(5).index:
        indices.append(i)

df = data.iloc[indices]

publishers_fig = px.treemap(df, path=['Publisher', 'Name'], values="Global_Sales")


top = pd.DataFrame(data.groupby("Name")[["Global_Sales"]].sum().sort_values(by=['Global_Sales'],ascending=[False]).reset_index())
pie1 = px.pie(top, values=top['Global_Sales'][:10], names=top['Name'][:10],title='Top 10 games globally',)

# pie1.show()



name2 = pd.DataFrame(data.groupby("Name")[["NA_Sales"]].mean().sort_values(by=['NA_Sales'],ascending=[False]).reset_index())
name2.rename(columns = {'Name':'Name_NA'}, inplace = True)

name3 = pd.DataFrame(data.groupby("Name")[["EU_Sales"]].mean().sort_values(by=['EU_Sales'],ascending=[False]).reset_index())
name3.rename(columns = {'Name':'Name_EU'}, inplace = True)

name4 = pd.DataFrame(data.groupby("Name")[["JP_Sales"]].mean().sort_values(by=['JP_Sales'],ascending=[False]).reset_index())
name4.rename(columns = {'Name':'Name_JP'}, inplace = True)

name5 = pd.DataFrame(data.groupby("Name")[["Other_Sales"]].mean().sort_values(by=['Other_Sales'],ascending=[False]).reset_index())
name5.rename(columns = {'Name':'Name_other'}, inplace = True)

#Concatenating the results.
name_df=pd.concat([name2,name3,name4,name5],axis=1)

subplot_name1 = make_subplots(rows=2, cols=2, shared_yaxes=True,subplot_titles=("North American top games","Europe top games", "Japan top games","Other regions top games",'Top games globally'))


#Subplot for North America
subplot_name1.add_trace(go.Bar(x=name_df['Name_NA'][:5], y=name_df['NA_Sales'][:5]),1, 1)

#Subplot for Europe
subplot_name1.add_trace(go.Bar(x=name_df['Name_EU'][:5], y=name_df['EU_Sales'][:5]), 1, 2)

#Subplot for Japan
subplot_name1.add_trace(go.Bar(x=name_df['Name_JP'][:5], y=name_df['JP_Sales'][:5]), 2, 1)

#Subplot for other regions
subplot_name1.add_trace(go.Bar(x=name_df['Name_other'][:5], y=name_df['Other_Sales'][:5]),2, 2)

subplot_name1.update_layout(height=1000,width=1400, showlegend=False)
subplot_name1.update_xaxes(tickangle=45)
# subplot_name1.show()


# --------------------------------------------------------------------------------#
# App Layout
# --------------------------------------------------------------------------------#
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])  # external_stylesheets = [dbc.themes.SLATE]
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Genre and Region sales visualization ",
                        className="text-center text-primary mb-4"),
                width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='region_sales_fig', figure=region_sales_fig)
        ], width={'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id='genre_sales_distribution_fig', figure=genre_sales_distribution_fig)
        ], width={'size': 5, 'offset': 0})

    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='genre_sales_fig', figure={})
        ], width={'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id='sales_over_time_fig', figure={})
        ], width={'size': 5, 'offset': 0})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='subplot_name1', figure=subplot_name1)
        ], width={'size': 15, 'offset': 1}),
    # dbc.Col([
    #         dcc.Graph(id='pie1', figure=pie1)
    #     ], width={'size': 5, 'offset': 1})

    ]),



    dbc.Row([
        dbc.Col(html.H1("Console and Manufacturer visualization",
                        className="text-center text-primary mb-4"),
                width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='console_timeline_fig', figure=console_timeline_fig)
        ], width={'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id='handheld_console_timeline_fig', figure=handheld_console_timeline_fig)
        ], width={'size': 5, 'offset': 1})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='manufacturer_timeline_figs', figure={}),
            dcc.Slider(step=None,
                       marks={
                           1980: '1980',
                           1990: '1990',
                           2000: '2000',
                           2010: '2010'},
                       value=1980,
                       id='manufacturer_timeline_slider'
                       )
        ], width={'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id='console_sales_fig', figure=consoles_sales_fig),
        ], width={'size': 5, 'offset': 1})
    ]),

    dbc.Row([
        dbc.Col(html.H1("Publishers sales visualization",
                        className="text-center text-primary mb-4"),
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='publishers_fig', figure=publishers_fig)
        ], width={'size': 10, 'offset': 1})
    ])
], fluid=True)








# --------------------------------------------------------------------------------#


# Update sales by genre figure when user selects region
# --------------------------------------------------------------------------------#
@app.callback(
    Output('genre_sales_fig', 'figure'),
    Input('region_sales_fig', 'selectedData')
)
def update_genre_graph(selectedData):
    if (selectedData != None and selectedData["points"][0]['label'] != "Global_Sales"):
        label = selectedData["points"][0]['y']
        fig = px.bar(genre_total_df, x="Genre", y=label, orientation='v',
                     text_auto=False, title=None, labels={"value": "Sales (in millions)"},
                     barmode='stack', color_discrete_sequence=[colors_dict[label]])
    else:
        label = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
        fig = px.bar(genre_total_df, x="Genre", y=label, orientation='v',
                     text_auto=False, title=None, labels={"value": "Sales (in millions)"},
                     barmode='stack', color_discrete_map=colors_dict)
    fig.update_layout(clickmode='event+select')

    return (fig)


# --------------------------------------------------------------------------------#


# Update sales over time figure when user selects region and genre
# --------------------------------------------------------------------------------#

@app.callback(
    Output('sales_over_time_fig', 'figure'),
    [Input('region_sales_fig', 'selectedData'),
     Input('genre_sales_fig', 'selectedData')]
)
def update_time_graph(regionSelectedData, genreSelectedData):
    region_label = regionSelectedData["points"][0]['label'] if regionSelectedData != None else "Global_Sales"
    region = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"] if region_label == "Global_Sales" else region_label
    genre = genreSelectedData["points"][0]['label'] if genreSelectedData != None else "All"
    title = genre
    if (genre != "All"):
        genre_df = data[data["Genre"] == genre]
        genre_df.groupby('Year').sum()
        fig = px.area(pd.DataFrame(genre_df.groupby('Year', as_index=False).sum()), x="Year", y=region,
                      labels={"value": "Sales ( in millions )"},
                      title=title,
                      color_discrete_map=colors_dict)
    else:
        genre_df = pd.DataFrame(data.groupby('Year', as_index=False).sum())
        fig = px.area(genre_df, x="Year", y=region,
                      labels={"value": "Sales ( in millions )"},
                      title=title,
                      color_discrete_map=colors_dict)

    return fig


# --------------------------------------------------------------------------------#

# Update manufacturer timeline chart when user change slider
# --------------------------------------------------------------------------------#
@app.callback(
    Output('manufacturer_timeline_figs', 'figure'),
    Input('manufacturer_timeline_slider', 'value'))
def update_output(value):
    if (value == 1980):
        return manufacturer_1980_fig
    elif (value == 1990):
        return manufacturer_1990_fig
    elif (value == 2000):
        return manufacturer_2000_fig
    else:
        return manufacturer_2010_fig


# --------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run_server(debug=True, port=3002)

###Show that pc games werent' popular in the 80s
###Show that some publishers are dominating
