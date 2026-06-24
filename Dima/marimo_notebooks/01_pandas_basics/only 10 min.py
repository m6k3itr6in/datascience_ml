import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    return np, pd


@app.cell
def _(np, pd):
    dates = pd.date_range("20130101", periods=6)

    dates 


    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df
    return dates, df


@app.cell
def _(dates, df):
    df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
    df1
    return (df1,)


@app.cell
def _(dates, df1):
    df1.loc[dates[0]:dates[1], "E"] = 1
    df1
    return


@app.cell
def _(df1):
    df1.dropna(how="any")
    return


@app.cell
def _(df1):
    df1.fillna(value='unknown')
    return


@app.cell
def _(df1, pd):
    pd.isna(df1)
    return


@app.cell
def _(df):
    df.mean()
    return


@app.cell
def _(df):
    df.mean(axis=1)
    return


@app.cell
def _(dates, df, np, pd):
    s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)
    s

    df.sub(s, axis="index")
    return


@app.cell
def _(df, np):
    df.agg(lambda x: np.mean(x) * 5.6)
    return


@app.cell
def _(df):
    df.transform(lambda x: x * 101.2)
    return


@app.cell
def _(np, pd):
    s1 = pd.Series(np.random.randint(0, 7, size=10))
    s1

    s1.value_counts()
    return


@app.cell
def _(np, pd):
    s2 = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])
    s2.str.lower()
    return


@app.cell
def _(np, pd):
    df2 = pd.DataFrame(np.random.randn(10, 4))
    df2
    return (df2,)


@app.cell
def _(df2, pd):
    pieces = [df2[:3], df2[3:7], df2[7:]]
    pd.concat(pieces)
    return


@app.cell
def _(pd):
    left = pd.DataFrame({'key':['foo', 'bar'], "lval":[1, 2]})
    right = pd.DataFrame({'key':['foo', 'bar'], 'rval':[4,5]})

    pd.merge(left, right, on='key')
    return


@app.cell
def _(np, pd):
    df3 = pd.DataFrame(
        {
            "A":['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
            "B":['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
            "C": np.random.randn(8),
            "D": np.random.randn(8),
        }
    )

    df3
    return (df3,)


@app.cell
def _(df3):
    df3.groupby("A")[["C", "D"]].sum()
    return


@app.cell
def _(df3):
    df3.groupby(["A", "B"]).sum()
    return


@app.cell
def _(np, pd):
    arrays = [
        ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
        ["one", "two", "one", "two", "one", "two", "one", "two"],
    ]

    index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])

    df4 = pd.DataFrame(np.random.randn(8, 2), index=index, columns=["A", "B"])

    df5 = df4[:4]

    df5

    stacked = df5.stack()

    stacked
    return (stacked,)


@app.cell
def _(stacked):
    stacked.unstack()
    return


@app.cell
def _(stacked):
    stacked.unstack(0)
    return


@app.cell
def _(np, pd):
    pivot = pd.DataFrame(
        {
            "A": ["one", "one", "two", "three"] * 3,
            "B": ["A", "B", "C"] * 4,
            "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 2,
            "D": np.random.randn(12),
            "E": np.random.randn(12),
        }
    )

    pivot
    return (pivot,)


@app.cell
def _(pd, pivot):
    pd.pivot_table(pivot, values="D", index=["A", "B"], columns="C")
    return


@app.cell
def _(np, pd):
    rng = pd.date_range("1/1/2012", periods=100, freq='s')

    ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)

    ts.resample("2Min").sum()
    return


@app.cell
def _(np, pd):
    rng1 = pd.date_range("3/6/2012 00:00", periods=5, freq="D")

    ts1 = pd.Series(np.random.randn(len(rng1)), rng1)

    ts1

    ts1_utc = ts1.tz_localize("UTC")

    rng1

    rng1 + pd.offsets.BusinessDay(16)
    return


@app.cell
def _(pd):
    df6 = pd.DataFrame(
        {"id":[1, 2, 3, 4, 5, 6], "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']}
    )

    df6["grade"] = df6["raw_grade"].astype("category")

    df6["grade"]

    new_categories = ["very good", "good", "very bad"]

    df6["grade"] = df6["grade"].cat.rename_categories(new_categories)

    df6["grade"] = df6["grade"].cat.set_categories(
        ["very bad", "bad", "medium", "good", "very good"]
    )

    df6.sort_values(by="grade", ascending=False)

    df6.groupby("grade", observed=False).size()
    return


@app.cell
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell
def _(plt):
    plt.close("all")
    return


@app.cell
def _(np, pd):
    ts2 = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))

    ts2 = ts2.cumsum()

    ts2.plot()
    return (ts2,)


@app.cell
def _(np, pd, plt, ts2):
    df7 = pd.DataFrame(np.random.randn(1000, 4), index=ts2.index, columns=["A", "B", "C", "D"])

    df7 = df7.cumsum()

    plt.figure()
    df7.plot()
    return


if __name__ == "__main__":
    app.run()
