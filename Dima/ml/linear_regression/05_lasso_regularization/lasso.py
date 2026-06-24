import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from sklearn.datasets import make_regression

    # 100 строк, 90 колонок. Но только 5 из них реально влияют на цену, остальные 85 - чистый шум!
    X_arr, y_arr = make_regression(n_samples=100, n_features=90, n_informative=5, noise=10.0, random_state=42)

    X = pd.DataFrame(X_arr)
    y = pd.Series(y_arr)
    return X, y


@app.cell
def _(X, y):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, Lasso
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    return (
        Lasso,
        X_test,
        X_train,
        mean_absolute_error,
        mean_squared_error,
        model,
        r2_score,
        y_pred,
        y_test,
        y_train,
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
    print((model.coef_ != 0).sum())
    return


@app.cell
def _(Lasso, X_test, X_train, r2_score, y_test, y_train):
    lasso = Lasso(alpha=1.0)

    lasso.fit(X_train, y_train)

    lasso_pred = lasso.predict(X_test)

    r2_score(y_true=y_test, y_pred=lasso_pred)
    return (lasso,)


@app.cell
def _(lasso):
    print((lasso.coef_ != 0).sum())
    return


if __name__ == "__main__":
    app.run()
