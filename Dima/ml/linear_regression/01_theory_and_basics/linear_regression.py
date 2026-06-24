import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    data = {
        "sq_meters": [30, 40, 50, 60, 80],
        "true_price": [100, 120, 150, 180, 220]
    }

    df_housing = pd.DataFrame(data)

    def calculate_mse(df: pd.DataFrame, w: float, b: float) -> float:
        predicted = df['sq_meters'] * w + b
        error = (df['true_price'] - predicted) ** 2

        return error.mean()

    calculate_mse(df_housing, 2.47297297, 25.40540540540539)
    return calculate_mse, df_housing, np, pd


@app.cell
def _(calculate_mse, df_housing):
    calculate_mse(df_housing, 3.0, 0)
    return


@app.cell
def _(df_housing):
    from sklearn.linear_model import LinearRegression 

    model = LinearRegression()

    model.fit(df_housing[['sq_meters']], df_housing['true_price'])

    model.coef_
    return LinearRegression, model


@app.cell
def _(model):
    model.intercept_
    return


@app.cell
def _(np, pd):
    # Генерируем 100 квартир
    np.random.seed(42)
    sq_meters = np.random.randint(20, 150, 100)

    # Истинная формула рынка: 2.5 тыс. за квадрат + 15 тыс. база + случайный шум (торг, ремонт)
    price = sq_meters * 2.5 + 15 + np.random.normal(0, 20, 100)

    df_real_estate = pd.DataFrame({'sq_meters': sq_meters, 'price': price})

    df_real_estate
    return (df_real_estate,)


@app.cell
def _(LinearRegression, df_real_estate):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    import matplotlib.pyplot as plt

    X = df_real_estate[['sq_meters']]
    y = df_real_estate['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model1 = LinearRegression()
    model1.fit(X_train, y_train)

    y_pred = model1.predict(X_test)

    mean_absolute_error(y_pred=y_pred, y_true=y_test)
    return X_test, mean_squared_error, plt, r2_score, y_pred, y_test


@app.cell
def _(mean_squared_error, y_pred, y_test):
    mean_squared_error(y_pred=y_pred, y_true=y_test)
    return


@app.cell
def _(r2_score, y_pred, y_test):
    r2 = r2_score(y_pred=y_pred, y_true=y_test)
    return (r2,)


@app.cell
def _(X_test, plt, r2, y_pred, y_test):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(X_test, y_test, label='Реальные цены (y_test)')
    ax.plot(X_test, y_pred, color='red', label='Предсказания модели (y_pred)')

    ax.set_title(f'Линейная регрессия. R2 = {round(r2, 3)}')
    ax.set_xlabel('Признак (X_test)')
    ax.set_ylabel('Цена (y)')
    ax.legend()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
