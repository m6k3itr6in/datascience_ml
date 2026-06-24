import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    n = 500
    # Бюджеты на рекламу в тысячах долларов
    tv_budget = np.random.uniform(10, 300, n)
    social_budget = np.random.uniform(5, 50, n)
    radio_budget = np.random.uniform(0, 100, n)

    # Истинная формула продаж (скрыта от аналитика шумом рынка)
    sales = (tv_budget * 3.0) + (social_budget * 5.0) + (radio_budget * 0.0) + 150 + np.random.normal(0, 30, n)

    df_marketing = pd.DataFrame({
        'tv_spend': tv_budget,
        'social_spend': social_budget,
        'radio_spend': radio_budget,
        'sales': sales
    })
    return (df_marketing,)


@app.cell
def _(df_marketing):
    df_marketing
    return


@app.cell
def _(df_marketing):
    df_marketing['social_spend'] = df_marketing['social_spend'] * 1000

    X = df_marketing[['tv_spend', 'social_spend', 'radio_spend']]

    y = df_marketing['sales']
    return X, y


@app.cell
def _(X, y):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.linear_model import LinearRegression 
    from sklearn.preprocessing import StandardScaler

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
