import numpy as np
import pandas as pd
import plotly.express as px
from dash import (Dash, dcc)
import dash_bootstrap_components as dbc

data = pd.read_csv("data/vgsales.csv")
fig = px.bar(data["Platform"].value_counts(), y='Platform', template="plotly_dark")

console_dict = {"platform": [], "start": [], "finish": [], "manufacture": []}



nintendo_home_video_game_console = ["NES", "SNES", "N64", "GC", "Wii", "WiiU"]
sony_home_video_game_console = ["PS", "PS2", "PS3", "PS4"]
microsoft_home_video_game_console = ["XB", "X360", "XOne"]
sega_home_video_game_console = ["GEN", "SCD","SAT","DC"]
atari_home_video_game_console = ["2600"]
nec_home_video_game_console = ["TG16", "PCFX"]
other_home_video_game_console = ["NG", "3DO"]

nintendo_handheld_game_console = ["GB", "GBA", "DS", "3DS"]
sony_handheld_game_console = ["PSP", "PSV"]
sega_handheld_game_console = ["GG"]
bandai_handheld_game_console = ["WS"]


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

fig_2 = px.timeline(
    console_df, x_start="start", x_end="finish", y="platform",
    color="manufacture", range_x=("1980-01-01", '2020-01-01'),
    title="Home Video Game Console",
    template="plotly_dark"
)


console_dict = {"platform":[], "start":[], "finish":[], "manufacture":[]}
add_to_dict("Nintendo", nintendo_handheld_game_console)
add_to_dict("Sony", sony_handheld_game_console)
add_to_dict("Sega", sega_handheld_game_console)
add_to_dict("Bandai", bandai_handheld_game_console)
console_df = pd.DataFrame(console_dict)

fig_3 = px.timeline(
    console_df, x_start="start", x_end="finish", y="platform",
    color="manufacture", range_x=("1980-01-01",'2022-01-01'),
    title="HandHeld Video Game Console",
    template="plotly_dark"
)
fig_3.update_yaxes(autorange="reversed")

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

import plotly.graph_objects as go
console_dict = {"manufacture":[], "number_of_game":[]}
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
pie_fig_1 = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7], title="Home Video Game Console 1980-1990", template="plotly_dark")

console_dict = {"manufacture":[], "number_of_game":[]}
add_to_dict("Nintendo", nintendo_home_video_game_console, query2)
add_to_dict("Sony", sony_home_video_game_console, query2)
add_to_dict("Microsoft", microsoft_home_video_game_console, query2)
add_to_dict("Sega", sega_home_video_game_console, query2)
add_to_dict("Atari", atari_home_video_game_console, query2)
add_to_dict("NEC", nec_home_video_game_console, query2)
add_to_dict("Other", other_home_video_game_console, query2)
console_df = pd.DataFrame(console_dict)
pie_fig_2 = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7], title="Home Video Game Console 1990-2000", template="plotly_dark")

console_dict = {"manufacture":[], "number_of_game":[]}
add_to_dict("Nintendo", nintendo_home_video_game_console, query3)
add_to_dict("Sony", sony_home_video_game_console, query3)
add_to_dict("Microsoft", microsoft_home_video_game_console, query3)
add_to_dict("Sega", sega_home_video_game_console, query3)
add_to_dict("Atari", atari_home_video_game_console, query3)
add_to_dict("NEC", nec_home_video_game_console, query3)
add_to_dict("Other", other_home_video_game_console, query3)
console_df = pd.DataFrame(console_dict)
pie_fig_3 = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7], title="Home Video Game Console 2000-2010", template="plotly_dark")

console_dict = {"manufacture":[], "number_of_game":[]}
add_to_dict("Nintendo", nintendo_home_video_game_console, query4)
add_to_dict("Sony", sony_home_video_game_console, query4)
add_to_dict("Microsoft", microsoft_home_video_game_console, query4)
add_to_dict("Sega", sega_home_video_game_console, query4)
add_to_dict("Atari", atari_home_video_game_console, query4)
add_to_dict("NEC", nec_home_video_game_console, query4)
add_to_dict("Other", other_home_video_game_console, query4)
console_df = pd.DataFrame(console_dict)
pie_fig_4 = px.pie(console_df, values='number_of_game', names='manufacture', color=[1, 2, 3, 4, 5, 6, 7], title="Home Video Game Console from 2010", template="plotly_dark")


if __name__ == '__main__':
    app.layout = dbc.Container([
        dbc.Row([

            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='fig', figure=fig)
            ], width={'size': 10, 'offset': 1})

        ]),
        dbc.Row([
            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='fig_2', figure=fig_2)
            ], width={'size': 10, 'offset': 1})


        ]),
        dbc.Row([
            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='fig_3', figure=fig_3)
            ], width={'size': 10, 'offset': 1})

        ]),
        dbc.Row([
            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='pie_fig_1', figure=pie_fig_1)
            ], width={'size': 5, 'offset': 1}),
            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='pie_fig_2', figure=pie_fig_2)
            ], width={'size': 5, 'offset': 1}),
            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='pie_fig_3', figure=pie_fig_3)
            ], width={'size': 5, 'offset': 1}),
            dbc.Col([
                # Sales by region figure
                dcc.Graph(id='pie_fig_4', figure=pie_fig_4)
            ], width={'size': 5, 'offset': 1}),

        ]),
    ], fluid=True)
    app.run_server(debug=True, port=3001)