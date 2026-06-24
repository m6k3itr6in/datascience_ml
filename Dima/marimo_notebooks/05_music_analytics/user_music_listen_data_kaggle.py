import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv('user_music_listen_data.csv', engine='pyarrow', dtype_backend='pyarrow')

    df = df.fillna(0).melt(id_vars='User_ID', var_name='Artist', value_name='Listen_Time').astype({'Artist':'category', 'Listen_Time':'int32[pyarrow]'})

    df_top_artists = df.groupby('Artist')[['Listen_Time']].sum().sort_values('Listen_Time', ascending=False)

    df_top_artists.head(3)

    df_top_users = df.groupby('User_ID')[['Listen_Time']].sum().sort_values('Listen_Time', ascending=False)

    df_top_users.head(5)

    df_top_artists['Listen_Time_Minutes'] = df_top_artists['Listen_Time'] / 60000

    df_top_artists.head(3)

    df_zero_listens = (df['Listen_Time'] > 0).sum()

    pd.DataFrame({
        'Zero_Listens': [df_zero_listens],
        'All_Listens': [len(df)],
    })
    return


if __name__ == "__main__":
    app.run()
