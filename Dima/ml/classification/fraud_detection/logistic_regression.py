import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    from sklearn.datasets import make_classification

    # Генерируем транзакции банка (несбалансированные классы)
    X_fraud, y_fraud = make_classification(
        n_samples=1000,        # 1000 транзакций
        n_features=3,          # 3 признака
        n_informative=2,       # 2 реально полезных признака
        n_redundant=1,         # 1 мусорный признак (для шума)
        weights=[0.9, 0.1],    # 90% честных (0), 10% фрод (1)
        random_state=42
    )

    # Переводим в Pandas для удобства
    X = pd.DataFrame(X_fraud, columns=['tx_amount_scaled', 'device_risk_score', 'location_trust'])
    y = pd.Series(y_fraud, name='is_fraud')
    return X, plt, y


@app.cell
def _(X):
    X
    return


@app.cell
def _(y):
    y
    return


@app.cell
def _(X, y):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import precision_score, recall_score, f1_score, PrecisionRecallDisplay

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(class_weight='balanced')

    model.fit(X_train, y_train)

    y_pred = model.predict_proba(X_test)

    y_probs = y_pred[:, 1]

    y_pred_custom = (y_probs >= 0.7).astype(int)
    return (
        PrecisionRecallDisplay,
        X_test,
        f1_score,
        model,
        precision_score,
        recall_score,
        y_pred_custom,
        y_test,
    )


@app.cell
def _(f1_score, precision_score, recall_score, y_pred_custom, y_test):
    print(f'Precision_score: {round(precision_score(y_true=y_test, y_pred=y_pred_custom), 2)}\nRecall_score: {round(recall_score(y_true=y_test, y_pred=y_pred_custom), 2)}\nF1_score: {round(f1_score(y_true=y_test, y_pred=y_pred_custom), 2)}')
    return


@app.cell
def _(PrecisionRecallDisplay, X_test, model, plt, y_test):
    fig, ax = plt.subplots()

    display = PrecisionRecallDisplay.from_estimator(estimator=model, X=X_test, y=y_test, ax=ax)

    ax.set_title('Precision Recall')
    ax.grid(True)
    plt.show()
    return


if __name__ == "__main__":
    app.run()
