import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _():
    import numpy as np

    return (np,)


@app.cell
def _(np, pd):
    np.random.seed(42)
    df = pd.DataFrame({
        "client_id": range(1, 1001),
        "age": np.random.randint(18, 70, size=1000),
        "salary": np.random.randint(30000, 250000, size=1000)
    })

    df
    return (df,)


@app.cell
def _(mo):
    salary_slider = mo.ui.slider(start=30000, stop=250000, step=10000, value=50000, label='Минимальная зарплата:')

    salary_slider
    return (salary_slider,)


@app.cell
def _(df, mo, salary_slider):
    filtered_df = df[df['salary'] >= salary_slider.value ]

    mo.md(f"**Найдено клиентов с зарплатой выше {salary_slider.value}:** {len(filtered_df)} человек.")
    return (filtered_df,)


@app.cell
def _(filtered_df):
    filtered_df.head(10)
    return


if __name__ == "__main__":
    app.run()
