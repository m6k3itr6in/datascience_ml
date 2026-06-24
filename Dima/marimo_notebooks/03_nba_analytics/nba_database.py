import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import sqlite3
    import plotly.express as px
    import matplotlib.pyplot as plt
    import seaborn as sns

    return pd, plt, px, sns, sqlite3


@app.cell
def _(sqlite3):
    conn = sqlite3.connect('nba.sqlite')
    return (conn,)


@app.cell
def _(conn, pd):
    query = """
    SELECT name 
    FROM sqlite_master 
    WHERE type='table' 
    ORDER BY name
    """

    pd.read_sql(sql=query, con=conn)
    return


@app.cell
def _(conn, pd):
    query2 = """
        SELECT * FROM team
        LIMIT 5
    """

    pd.read_sql(sql=query2, con=conn)
    return


@app.cell
def _(conn, pd):
    query3 = """
        SELECT full_name, year_founded
        FROM team
        WHERE year_founded IS NOT NULL
        ORDER BY year_founded ASC
        LIMIT 3
    """

    pd.read_sql(sql=query3, con=conn)
    return


@app.cell
def _(conn, pd):
    query4 = """
        SELECT * FROM game LIMIT 5
    """

    pd.read_sql(sql=query4, con=conn)
    return


@app.cell
def _(conn, pd):
    query_join = """
        SELECT full_name, COUNT(wl_home) AS matches, ROUND(AVG(CASE WHEN wl_home = 'W' THEN 1.0 ELSE 0.0 END) * 100, 2) AS win_pct
        FROM team
        JOIN game ON game.team_id_home = team.id
        GROUP BY full_name
        HAVING COUNT(game_id) >= 100
        ORDER BY win_pct DESC
        LIMIT 5
    """

    pd.read_sql(sql=query_join, con=conn, dtype_backend='pyarrow')
    return


@app.cell
def _(conn, pd):
    query_cte = """
        WITH team_stats AS (
            SELECT full_name, COUNT(wl_home) AS matches, ROUND(AVG(CASE WHEN wl_home = 'W' THEN 1.0 ELSE 0.0 END) * 100, 1) AS win_pct
            FROM team
            JOIN game ON game.team_id_home = team.id
            GROUP BY full_name
            HAVING COUNT(game_id) >= 100
        )

        SELECT full_name, matches, win_pct, RANK() OVER(ORDER BY win_pct DESC) AS rank
        FROM team_stats
        LIMIT 5
    """

    # или так

    query_cte2 = """
        WITH team_stats AS (
            SELECT full_name, COUNT(wl_home) AS matches, ROUND(AVG(CASE WHEN wl_home = 'W' THEN 1.0 ELSE 0.0 END) * 100, 1) AS win_pct
            FROM team
            JOIN game ON game.team_id_home = team.id
            GROUP BY full_name
            HAVING COUNT(game_id) >= 100
        ),

        all_ranks AS (
            SELECT full_name, matches, win_pct, RANK() OVER(ORDER BY win_pct DESC) AS rank
            FROM team_stats
        )

        SELECT * FROM all_ranks
        WHERE rank <= 5
    """

    pd.read_sql(sql=query_cte2, con=conn, index_col='rank', dtype_backend='pyarrow')
    return


@app.cell
def _(conn, pd, px):
    query_3_score = """
        SELECT SUBSTR(game_date, 1, 4) AS year, ROUND(AVG(fg3a_home + fg3a_away), 2) AS avg_fg3a
        FROM game
        WHERE fg3a_home IS NOT NULL AND fg3a_away IS NOT NULL
        GROUP BY year
        ORDER BY year ASC
    """

    df3_pt = pd.read_sql(sql=query_3_score, con=conn, dtype_backend='pyarrow')

    graph = px.line(df3_pt, x='year', y='avg_fg3a', title='Ср. кол-во 3-х очковых бросков за год', labels={"year":"Год", "avg_fg3a":"Броски"}, template='plotly_white')

    graph
    return (df3_pt,)


@app.cell
def _(df3_pt, plt):
    df3_pt['year'] = df3_pt['year'].astype('int32[pyarrow]')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df3_pt['year'], df3_pt['avg_fg3a'], color='black')
    ax.set_title('Ср. кол-во 3-х очковых бросков за год')
    ax.set_xlabel('Год')
    ax.set_ylabel('Броски')
    ax.grid(True)
    ax.tick_params(axis='x', rotation=45)

    ax
    return


@app.cell
def _(conn, pd, plt, sns):
    query5 = """
        SELECT full_name, AVG(CASE WHEN wl_home = 'W' THEN 1.0 ELSE 0.0 END) as winrate, SUBSTR(game_date, 1, 4) AS year
        FROM game
        JOIN team ON team.id = game.team_id_home
        WHERE game_date BETWEEN '2014-01-01' AND '2023-12-31'
        GROUP BY full_name, year
        ORDER BY winrate DESC
    """

    df_all = pd.read_sql(sql=query5, con=conn, dtype_backend='pyarrow')

    df_team_avg = df_all.groupby('full_name')['winrate'].mean()

    bad_teams = df_team_avg[df_team_avg < 0.5].index

    df_bad_teams = df_all[df_all['full_name'].isin(bad_teams)]

    df_bad_teams = df_bad_teams.copy()
    df_bad_teams['year'] = df_bad_teams['year'].astype('int32')
    df_bad_teams['winrate'] = df_bad_teams['winrate'].astype('float64')

    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(12, 6))

    plot = sns.lineplot(data=df_bad_teams, x='year', y='winrate', hue='full_name', marker='o')

    sns.move_legend(plot, 'upper left', bbox_to_anchor=(1, 1))

    plot.set_title("Динамика процента побед проблемных команд (2014-2023)", fontsize=14, pad=20)
    plot.set_xlabel("Сезон", fontsize=12)
    plot.set_ylabel("Процент побед (WinRate)", fontsize=12)

    sns.despine()

    plt.show()
    return


if __name__ == "__main__":
    app.run()
