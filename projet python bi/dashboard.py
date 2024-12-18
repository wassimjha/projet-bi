import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go

# Load cleaned data
daily_scores = pd.read_csv("daily_scores_clean.csv")
league_standings = pd.read_csv("league_standings_clean.csv")
player_stats = pd.read_csv("player_stats_clean.csv")

# Find the best players for each stat
best_players = {
    stat: player_stats.loc[player_stats[stat].idxmax(), ['Player Name', stat]]
    for stat in ["PTS", "TRB", "AST", "STL", "BLK", "TOV", "PF", "FG", "FT", "3P"]
}

# Map full stat names for display
stat_full_names = {
    "PTS": "Points",
    "TRB": "Total Rebounds",
    "AST": "Assists",
    "STL": "Steals",
    "BLK": "Blocks",
    "TOV": "Turnovers",
    "PF": "Personal Fouls",
    "FG": "Field Goals",
    "FT": "Free Throws",
    "3P": "Three-Point Shots"
}

# Initialize the Dash app
app = Dash(__name__)
app.title = "NBA Dashboard"

# Define app layout
app.layout = html.Div([

    # Sidebar
    html.Div([
        # Sidebar Header
        html.H2("Player Search", style={"marginBottom": "20px", "color": "#ffffff"}),

        # Search bar
        dcc.Dropdown(
            id="player-search",
            options=[{"label": player, "value": player} for player in player_stats['Player Name']],
            placeholder="Search for a player",
            style={
                "width": "100%", "padding": "10px", "fontSize": "18px",
                "color": "#333333", "cursor": "pointer"
            }
        ),

        # Button to show player stats
        html.Button("Show Player Stats", id="show-stats-btn", n_clicks=0, style={
            "marginTop": "20px", "padding": "10px", "fontSize": "16px", "width": "100%",
            "backgroundColor": "#C9082A", "color": "#ffffff", "border": "none",
            "borderRadius": "5px", "cursor": "pointer", "transition": "0.3s"
        }),

    ], style={
        "padding": "20px", "backgroundColor": "#17408B", "width": "250px", "height": "100vh",
        "position": "fixed", "boxShadow": "2px 0 5px rgba(0, 0, 0, 0.2)"
    }),

    # Top-right NBA Logo
    html.Div([
        html.Img(
            src="/assets/nba-logo.ico",  # Ensure the logo is in the 'assets' folder
            style={
                "width": "100px", "position": "absolute", "top": "30px", "right": "20px"
            }
        )
    ]),

    # Main Content
    html.Div([
        html.H1("NBA Dashboard", style={
            "textAlign": "center", "marginBottom": "20px", "color": "#1F77B4",
            "fontSize": "2.5rem", "fontWeight": "bold"
        }),

        # Section: Last night's games
        html.H2("Latest NBA Games", style={"textAlign": "center", "marginBottom": "20px"}),
        html.Div([
            html.Div([
                html.H4(f"{row['Away Team']} VS {row['Home Team']}",
                        style={"textAlign": "center", "marginBottom": "10px", "color": "#333"}),
                html.H4(f"{row['Away Score']} - {row['Home Score']}",
                        style={"textAlign": "center", "marginBottom": "10px", "color": "#333"}),
                html.Button("Show Game Stats", id=f"game-stats-btn-{index}", n_clicks=0, style={
                    "backgroundColor": "#1F77B4", "color": "#ffffff", "padding": "10px",
                    "border": "none", "borderRadius": "5px", "cursor": "pointer", "width": "100%",
                    "transition": "0.3s"
                })
            ], style={
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)", "borderRadius": "10px",
                "padding": "15px", "margin": "10px", "backgroundColor": "#ffffff",
                "textAlign": "center", "width": "300px"
            })
            for index, row in daily_scores.iterrows()
        ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "space-around"}),

        # Section: League Standings
        html.H2("League Standings", style={"textAlign": "center", "marginTop": "30px", "marginBottom": "20px"}),
        dcc.Dropdown(
            id="conference-dropdown",
            options=[
                {"label": "Eastern Conference", "value": "Eastern Conference"},
                {"label": "Western Conference", "value": "Western Conference"},
            ],
            value="Eastern Conference",
            style={"width": "50%", "margin": "0 auto", "fontSize": "18px"}
        ),
        dcc.Graph(id="standings-graph", style={"marginTop": "40px"}),

        # Player Stats Dashboards Section
        html.Div(id="player-stats-section", style={"marginTop": "50px", "padding": "20px"}),

        # Game Stats Section (Will be populated dynamically)
        html.Div(id="game-stats-section", style={"marginTop": "50px", "padding": "20px"})

    ], style={"marginLeft": "270px", "padding": "20px"})
])

# Custom hover styling
app.index_string = """
<!DOCTYPE html>
<html>
<head>
    <title>NBA Dashboard</title>
    <style>
        button:hover {
            background-color: #155D8A !important;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""
# Callback to show game stats on button click
@app.callback(
    Output("game-stats-section", "children"),
    [Input(f"game-stats-btn-{i}", "n_clicks") for i in range(len(daily_scores))],
    prevent_initial_call=True
)
def show_game_stats(*args):
    # Get the index of the button that was clicked
    clicked_index = next((i for i, n_clicks in enumerate(args) if n_clicks > 0), None)

    if clicked_index is None:
        return html.Div([])  # Return empty div if no button is clicked

    # Extract the clicked game data
    game_data = daily_scores.iloc[clicked_index]

    # Comparison Bar Chart: Points
    points_comparison_chart = dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    name=game_data['Home Team'],
                    x=['Points', 'Rebounds', 'Assists'],
                    y=[
                        game_data.get('Home Score', 0),
                        game_data.get('Home TRB', 0),
                        game_data.get('Home AST', 0)
                    ],
                    textposition='outside',
                    marker_color='#FF5733'
                ),
                go.Bar(
                    name=game_data['Away Team'],
                    x=['Points', 'Rebounds', 'Assists'],
                    y=[
                        game_data.get('Away Score', 0),
                        game_data.get('Away TRB', 0),
                        game_data.get('Away AST', 0)
                    ],
                    textposition='outside',
                    marker_color='#3498DB'
                )
            ],
            layout=go.Layout(
                title="Points, Rebounds, and Assists Comparison",
                barmode='group',
                template="plotly_dark",
                height=350
            )
        )
    )

    # Shooting Efficiency Comparison Pie Charts
    shooting_efficiency_chart_home = dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(
                    labels=['Field Goals', '3-Pointers', 'Free Throws'],
                    values=[
                        game_data.get('Home FG', 0),
                        game_data.get('Home 3P', 0),
                        game_data.get('Home FT', 0)
                    ],
                    textinfo='label+percent',
                    hole=0.3
                )
            ],
            layout=go.Layout(
                title=f"{game_data['Home Team']} Shooting Efficiency",
                template="plotly_dark",
                height=300
            )
        )
    )

    shooting_efficiency_chart_away = dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(
                    labels=['Field Goals', '3-Pointers', 'Free Throws'],
                    values=[
                        game_data.get('Away FG', 0),
                        game_data.get('Away 3P', 0),
                        game_data.get('Away FT', 0)
                    ],
                    textinfo='label+percent',
                    hole=0.3
                )
            ],
            layout=go.Layout(
                title=f"{game_data['Away Team']} Shooting Efficiency",
                template="plotly_dark",
                height=300
            )
        )
    )

    # Key Stats Comparison Chart
    key_stats_chart = dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    name=game_data['Home Team'],
                    x=['Steals', 'Blocks', 'Turnovers', 'Fouls'],
                    y=[
                        game_data.get('Home STL', 0),
                        game_data.get('Home BLK', 0),
                        game_data.get('Home TOV', 0),
                        game_data.get('Home PF', 0)
                    ],
                    marker_color='#FF5733'
                ),
                go.Bar(
                    name=game_data['Away Team'],
                    x=['Steals', 'Blocks', 'Turnovers', 'Fouls'],
                    y=[
                        game_data.get('Away STL', 0),
                        game_data.get('Away BLK', 0),
                        game_data.get('Away TOV', 0),
                        game_data.get('Away PF', 0)
                    ],
                    marker_color='#3498DB'
                )
            ],
            layout=go.Layout(
                title="Key Stats Comparison",
                barmode='group',
                template="plotly_dark",
                height=350
            )
        )
    )

    # Return the updated grid layout with comparisons
    return html.Div([
        html.H3(f"Game Stats: {game_data['Away Team']} vs {game_data['Home Team']}", 
                style={"textAlign": "center", "marginBottom": "20px"}),

        # Grid Layout
        html.Div([
            html.Div(points_comparison_chart, style={'padding': '10px', 'borderRadius': '10px'}),
            html.Div(key_stats_chart, style={'padding': '10px', 'borderRadius': '10px'}),
            html.Div(shooting_efficiency_chart_home, style={'padding': '10px', 'borderRadius': '10px'}),
            html.Div(shooting_efficiency_chart_away, style={'padding': '10px', 'borderRadius': '10px'})
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(2, 1fr)',
            'gap': '20px',
            'margin': '20px'
        })
    ])


# Callback to update league standings
@app.callback(
    Output("standings-graph", "figure"),
    Input("conference-dropdown", "value")
)
def update_standings_graph(conference):
    filtered_df = league_standings[league_standings["Conference"] == conference]
    filtered_df = filtered_df.sort_values(by='Wins', ascending=False)

    # Alternate colors between blue and orange
    colors = ['#1F77B4' if i % 2 == 0 else '#FF7F0E' for i in range(len(filtered_df))]
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=filtered_df['Team'],
                y=filtered_df['Wins'],
                marker=dict(color=colors)
            )
        ],
        layout=go.Layout(
            title=f"Standings - {conference}",
            xaxis={'title': 'Teams'},
            yaxis={'title': 'Wins'},
            height=400
        )
    )
    return fig

# Callback to show player stats with gauge chart and pie chart
@app.callback(
    Output("player-stats-section", "children"),
    Input("show-stats-btn", "n_clicks"),
    State("player-search", "value")
)
def show_player_stats(n_clicks, selected_player):
    if not selected_player:
        return html.Div("Please select a player first.", style={"fontSize": "18px", "color": "red"})

    player_data = player_stats[player_stats["Player Name"] == selected_player].iloc[0]
    charts = []

    for stat, full_name in stat_full_names.items():
        best_player_name = best_players[stat]['Player Name']
        best_value = best_players[stat][stat]
        player_value = player_data[stat]

        # Gauge and Pie Charts Side by Side
        charts.append(html.Div([
            html.H4(f"{full_name} (Best Player: {best_player_name})", style={"marginBottom": "10px"}),
            html.Div([
                dcc.Graph(figure=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=player_value,
                    title={"text": full_name},
                    gauge={'axis': {'range': [0, max(best_value, player_value)]}}
                )), style={"width": "45%"}),

                dcc.Graph(figure=go.Figure(data=[go.Pie(
                    labels=[selected_player, f"{best_player_name}"],
                    values=[player_value, best_value],
                    marker=dict(colors=["#1f77b4", "#ff7f0e"])
                )]), style={"width": "45%"}),
            ], style={"display": "flex", "justifyContent": "space-between"})
        ], style={"marginBottom": "30px", "padding": "20px", "boxShadow": "0 4px 8px rgba(0,0,0,0.2)", "borderRadius": "10px", "backgroundColor": "#ffffff"}))

    return html.Div([
        html.H3(f"Player Stats: {selected_player}", style={"textAlign": "center", "marginBottom": "30px"}),
        *charts
    ])

# Button callback for each game in the daily_scores data
@app.callback(
    Output("game-stats-btn-0", "children"),
    Input("game-stats-btn-0", "n_clicks"),
    [State("game-stats-btn-0", "id")]
)
def update_game_button_text(n_clicks, btn_id):
    if n_clicks > 0:
        return "Stats Loaded"
    return "Show Game Stats"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
