import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    df_insurance = pd.read_csv('insurance.csv', engine='pyarrow')

    df = pd.get_dummies(data=df_insurance, drop_first=True, dtype=int)

    df
    return (df,)


@app.cell
def _(df):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import StandardScaler

    X = df.drop(['charges'], axis=1)

    y = df['charges']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = scaler.transform(X_test)

    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    return (
        mean_absolute_error,
        mean_squared_error,
        model,
        r2_score,
        y_pred,
        y_test,
    )


@app.cell
def _(mean_absolute_error, y_pred, y_test):
    mean_absolute_error(y_true=y_test, y_pred=y_pred)
    return


@app.cell
def _(mean_squared_error, y_pred, y_test):
    mean_squared_error(y_true=y_test, y_pred=y_pred) ** 0.5
    return


@app.cell
def _(r2_score, y_pred, y_test):
    r2_score(y_true=y_test, y_pred=y_pred)
    return


@app.cell
def _(model):
    model.coef_
    return


if __name__ == "__main__":
    app.run()
