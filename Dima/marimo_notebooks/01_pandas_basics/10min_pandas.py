import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    return np, pd


@app.cell
def _(np, pd):
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    s
    return


@app.cell
def _(np, pd):
    dates = pd.date_range("20130101", periods=6)
    dates

    my_custom_data = [[10,15,20,25],
                      [30,35,40,45],
                      [50,55,60,65],
                      [70,75,80,85],
                      [90,95,10,15],
                      [20,25,30,35]]

    df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list("ABCD"), dtype="float32[pyarrow]")

    df
    return dates, df


@app.cell
def _(pd):
    df2 = pd.DataFrame(
        {
            "A":pd.Series(1.0, index=list(range(100000)), dtype="float32"),
            "B":pd.Timestamp("20130102"),
            "C":pd.Series(1, index=list(range(100000)), dtype="float32"),
            "D":3,
            "F":pd.Series([f"foo_{i}" for i in range(100000)], dtype="string[pyarrow]"),
        })

    df_old = pd.DataFrame({
            "A":pd.Series(1.0, index=list(range(100000)), dtype="float32"),
            "B":pd.Timestamp("20130102"),
            "C":pd.Series(1, index=list(range(100000)), dtype="float32"),
            "D":3,
            "F":pd.Series([f"foo_{i}" for i in range(100000)], dtype="object"),
    })
    return df2, df_old


@app.cell
def _(df2, df_old):
    df2.info(memory_usage="deep")
    df_old.info(memory_usage="deep")
    return


@app.cell
def _(df2):
    df2.to_csv('data.csv', index=False)
    df2.to_parquet('data.parquet')
    return


@app.cell
def _(pd):
    df_csv = pd.read_csv('data.csv')
    df_parquet = pd.read_parquet('data.parquet')

    df_csv.dtypes
    return (df_parquet,)


@app.cell
def _(df_parquet):
    df_parquet.dtypes
    return


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    df.tail(1)
    return


@app.cell
def _(df):
    df.index
    return


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    df.to_numpy()
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell
def _(df):
    df.T
    return


@app.cell
def _(df):
    df.sort_index(axis=1, ascending=False)
    return


@app.cell
def _(df):
    df.sort_values(by="C")
    return


@app.cell
def _(df):
    df["20130102":"20130104"]
    return


@app.cell
def _(dates, df):
    df.loc[dates[0]]
    return


@app.cell
def _(df):
    df.loc[:, ["A", "B"]]
    return


@app.cell
def _(df):
    df.loc["20130102":"20130104", ["A", "B"]]
    return


@app.cell
def _(dates, df):
    df.loc[dates[0], "A"]
    return


@app.cell
def _(df):
    df.iloc[3]
    return


@app.cell
def _(df):
    df.iloc[3, 2]
    return


@app.cell
def _(df):
    df.iloc[3:5, 1:3]
    return


@app.cell
def _(df):
    df.iloc[[1, 2, 4], [0, 2]]
    return


@app.cell
def _(df):
    df_copy = df.copy()
    return (df_copy,)


@app.cell
def _(df_copy):
    df_copy["E"] = ["one", "one", "two", "three", "four", "three"]
    df_copy
    return


@app.cell
def _(df_copy):
    df_copy[df_copy["E"].isin(["two", "four"])]
    return


@app.cell
def _(pd):
    s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range("20130102", periods=6))
    s1
    return (s1,)


@app.cell
def _(df, s1):
    df["F"] = s1
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(dates, df):
    df.at[dates[0], "A"] = 0
    return


@app.cell
def _(df):
    df.iat[0, 1] = 0
    return


@app.cell
def _(df, np):
    df.loc[:, "D"] = np.array([5] * len(df))
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    df_copy1 = df.copy()
    df_copy1[df_copy1 > 0] = -df_copy1
    return (df_copy1,)


@app.cell
def _(df_copy1):
    df_copy1
    return


@app.cell
def _(np, pd):
    s2 = pd.Series([1, 2, np.nan])
    s2
    return


@app.cell
def _(np, pd):
    s3 = pd.Series([1, 2, np.nan], dtype="int64[pyarrow]")
    s3
    return


@app.cell
def _():
    import time
    raw_data = ["foo"] * 1000000
    return raw_data, time


@app.cell
def _():
    return


@app.cell
def _(np, pd, raw_data, time):
    df7 = pd.DataFrame({
        'A':pd.Series(np.random.randn(1000000)),
        'F':pd.Series(raw_data, dtype='string[pyarrow]')
    })
    start = time.time()
    df7[(df7['A'] > 0) & (df7['F'].str.startswith('foo'))]
    end = time.time()

    print(end-start)
    return (df7,)


@app.cell
def _(df7, time):
    df7['F'] = df7['F'].astype('object')

    start1 = time.time()
    df7[(df7['A'] > 0) & (df7['F'].str.startswith('foo'))]
    end1 = time.time()

    print(end1 - start1)
    return


@app.cell
def _(pd):
    data = {
        'A': [1, 2, None, 4, 5, None, 7, 8, 9, 10],
        'B': ['яблоко', None, 'банан', 'вишня', None, 'дыня', 'ежевика', 'инжир', 'груша', 'киви']
    }
    df_miss = pd.DataFrame({
        'A': pd.Series(data['A'], dtype='int64[pyarrow]'),
        'B': pd.Series(data['B'], dtype='string[pyarrow]'),
    })

    df_miss.fillna({'A':0, 'B':'unknown'})
    return


@app.cell
def _(pd):
    df_users = pd.DataFrame({
        'user_id': pd.Series([0, 1, 2], dtype='int64[pyarrow]'),
        'name': pd.Series(['Alice', 'Bob', 'Charlie'], dtype='string[pyarrow]'),
    })
    df_users

    df_sales = pd.DataFrame({
        'user_id': pd.Series(list('12133'), dtype='int64[pyarrow]'),
        'amount': pd.Series([100, 200, 150, 300, 50])
    })

    df_merged = pd.merge(df_users, df_sales, on='user_id', how='outer').fillna({'amount':0, 'name':'unknown'}).groupby(by=['name'])[['amount']].sum()

    df_merged
    return


@app.cell
def _(pd):
    df_pivot = pd.DataFrame({
        "user_id": pd.Series([1, 1, 2, 2]),
        "category": pd.Series(['Electronics', 'Books', 'Electronics', 'Books'], dtype='string[pyarrow]'),
        "price": pd.Series([1000, 200, 500, 150])
    })

    pd.pivot_table(df_pivot, values='price', index='user_id', columns='category', aggfunc='sum', margins=True)
    return


@app.cell
def _(pd):
    df_wide = pd.DataFrame({
        'user_id': pd.Series([1, 2]),
        'Books': pd.Series([200, 150]),
        'Electronics': pd.Series([1000, 500]),
    })

    df_wide.melt(id_vars=['user_id'], var_name='category', value_name='amount').astype({'category':'category', 'amount':'int32[pyarrow]'})
    return


@app.cell
def _(np, pd):
    index = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')

    df_time = pd.DataFrame({
        'sales':np.random.randint(10, 100, len(index))
    }, index=index)

    df_time.resample("W").sum()
    return


if __name__ == "__main__":
    app.run()
