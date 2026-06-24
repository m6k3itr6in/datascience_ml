import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import io

    return io, pd


@app.cell
def _():
    dirty_rookies_dict = {
        "player_info":["Victor Wembanyama_Center", "Scoot Henderson_Guard", "Brandon Miller_Forward", "  Amen Thompson_Guard  "],
        "draft_year":["2023", "2023", "2023", "2023"],
        "college_or_team":["Metropolitans 92", "G League Ignite", "Alabama", None]
    }


    dirty_stats_csv = """PlayerName|PTS|REB|AST|Turnovers|
    LeBron James|28.9|8.3|6.8|3.2|
    Kevin Durant|29.1|6.7|5.0|3.3|
    Lebron  James|28.9|8.3|6.8|3.2|
    Stephen Curry|29.4|6.1|6.3||
    Joel Embiid|33.1|10.2|4.2|3.4|"""
    return dirty_rookies_dict, dirty_stats_csv


@app.cell
def _(dirty_rookies_dict, pd):
    df_rookies = (
        pd.DataFrame(data = dirty_rookies_dict, dtype='string[pyarrow]')
            .rename(columns={'player_info':'name'})
            .assign(name=lambda x: x['name']
                .str.split('_')
                .str[0]
                .str.strip()
                .astype('string[pyarrow]')
                   )
    )

    df_rookies
    return (df_rookies,)


@app.cell
def _(dirty_stats_csv, io, pd):
    df_stats = (
        pd.read_csv(io.StringIO(dirty_stats_csv), sep='|', dtype_backend='pyarrow')
            .drop(columns='Unnamed: 5')
            .assign(
                PlayerName=lambda x: x['PlayerName']
                    .str.replace(r'\s+', ' ', regex=True)
                    .str.strip()
                    .str.title()
            )
            .drop_duplicates(subset=['PlayerName'])
            .assign(
                Turnovers=lambda x: round(x['Turnovers'].fillna(x['Turnovers'].mean()), 3)
            )
    )
    return (df_stats,)


@app.cell
def _(df_rookies, df_stats, pd):
    with pd.ExcelWriter('nba_clean_report.xlsx') as writer:
        df_rookies.to_excel(writer, sheet_name='Draft_2023', index=False)
        df_stats.to_excel(writer, sheet_name='Players_Stats', index=False)
    return


@app.cell
def _():
    dirty_tickets =[
        {" game_id ": "G001", " arena ": " Madison Square Garden ", "sold_seats": "19,500"},
        {" game_id ": "G002", " arena ": "Staples Center", "sold_seats": "18997"},
        {" game_id ": "G003", " arena ": "  United Center  ", "sold_seats": "None"},
        {" game_id ": "G001", " arena ": " Madison Square Garden ", "sold_seats": "19,500"} # Полный дубликат
    ]

    dirty_merch_csv = """date|item|revenue
    2023-10-25|Jersey|$1,250.00
    10/26/2023|Hat|$450.75
    2023-10-27||$3,100.50
    invalid_date|Mug|$50.00
    2023-10-29|Jersey|$1,250.00"""
    return dirty_merch_csv, dirty_tickets


@app.cell
def _(dirty_tickets, pd):
    df_tickets = (
        pd.DataFrame(data=dirty_tickets, dtype='string[pyarrow]')
            .rename(str.strip, axis=1)
            .assign(arena=lambda x: x['arena'].str.strip())
            .assign(sold_seats=lambda x: x['sold_seats']
                .str.replace(',', '', regex=True)
                .replace('None', pd.NA, regex=True)
                .astype('int64[pyarrow]'))
            .drop_duplicates()
    )

    df_tickets
    return (df_tickets,)


@app.cell
def _(dirty_merch_csv, io, pd):
    df_merch = (
        pd.read_csv(io.StringIO(dirty_merch_csv), sep='|', dtype_backend='pyarrow')
            .assign(
                revenue=lambda x: x['revenue']
                    .str.replace(r'[\$,]', '', regex=True)
                    .astype('float[pyarrow]'),
                item=lambda x: x['item'].fillna(value='Unknown'),
                date=lambda x: pd
                    .to_datetime(x['date'], errors='coerce', format='mixed')
                    .astype('timestamp[ns][pyarrow]')
                   )
    )

    df_merch
    return (df_merch,)


@app.cell
def _(df_merch, df_tickets):
    df_tickets.to_csv('tickets_clean.csv', index=False, sep=';')
    df_merch.to_csv('merch_clean.csv', index=False, sep=';')
    return


if __name__ == "__main__":
    app.run()
