import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    np.random.seed(100)
    n = 800

    # Генерируем фичи
    true_1 = np.random.normal(0, 1, n)
    true_2 = np.random.normal(0, 1, n)

    # Мультиколлинеарность (копии с шумом)
    corr_1a = true_1 + np.random.normal(0, 0.01, n)
    corr_1b = true_1 + np.random.normal(0, 0.01, n)
    corr_2a = true_2 + np.random.normal(0, 0.01, n)

    # Мусорные фичи (чистый шум)
    garbage = np.random.normal(0, 1, (n, 15))

    # Целевая переменная (зависит только от true_1 и true_2)
    z = 1.5 * true_1 - 2.0 * true_2
    prob = 1 / (1 + np.exp(-z))
    y = np.random.binomial(1, prob)

    # Собираем датафрейм
    columns = ['true_1', 'true_2', 'corr_1a', 'corr_1b', 'corr_2a'] + [f'noise_{i}' for i in range(15)]
    X_data = np.hstack([true_1.reshape(-1, 1), true_2.reshape(-1, 1), corr_1a.reshape(-1, 1), corr_1b.reshape(-1, 1), corr_2a.reshape(-1, 1), garbage])
    df = pd.DataFrame(X_data, columns=columns)
    df['target'] = y

    df.to_csv('regularization_battle.csv', index=False)
    return (pd,)


@app.cell
def _(pd):
    from sklearn.linear_model import LogisticRegression, Lasso, Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    def prepare_data(filepath: str) -> tuple:
        df_data = pd.read_csv(filepath, engine='pyarrow')

        X = df_data.drop(columns=['target'])
        y = df_data['target']

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        feature_names = X.columns

        return X_train_scaled, X_test_scaled, y_train, y_test, feature_names

    return LogisticRegression, prepare_data


@app.cell
def _(pd):
    def train_and_get_coefs(model, X_train, y_train, feature_names: list[str]) -> pd.Series:
        model.fit(X_train, y_train)

        return pd.Series(model.coef_[0], index=feature_names)

    return (train_and_get_coefs,)


@app.cell
def _(LogisticRegression, pd, prepare_data, train_and_get_coefs):

    X_train, X_test, y_train, y_test, feature_names = prepare_data('Dima/ml/linear_regression/07_regularization/regularization_battle.csv')

    models_to_test = {
        'No Regularization': LogisticRegression(penalty=None, max_iter=1000),
        'Lasso (L1): C = 0.01': LogisticRegression(penalty='l1', solver='liblinear', C=0.01, random_state=42),
        'Lasso (L1): C = 0.1': LogisticRegression(penalty='l1', solver='liblinear', C=0.1, random_state=42),
        'Lasso (L1): C = 100.0': LogisticRegression(penalty='l1', solver='liblinear', C=100.0, random_state=42),
        'Ridge (L2): C = 0.01': LogisticRegression(penalty='l2', C=0.01, random_state=42),
        'Ridge (L2): C = 0.1': LogisticRegression(penalty='l2', C=0.1, random_state=42),
        'Ridge (L2): C = 100.0': LogisticRegression(penalty='l2', C=100.0, random_state=42),
        'ElasticNet (L1 + L2): C = 0.1, L1 & L2 = 0.5': LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, C=0.1, random_state=42, max_iter=5000)
    }

    results = {}
    for name, model in models_to_test.items():
        results[name] = train_and_get_coefs(model, X_train, y_train, feature_names)

    df_comparison = pd.DataFrame(results)
    df_comparison
    return


if __name__ == "__main__":
    app.run()
