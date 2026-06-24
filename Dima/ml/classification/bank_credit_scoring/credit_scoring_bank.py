import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    np.random.seed(42)

    def generate_credit_data(n, is_prod=False):
        # Генерируем фичи
        data = {
            'client_id': range(1000, 1000 + n) if not is_prod else range(9000, 9000 + n),
            'age': np.random.randint(18, 70, n),
            'income_usd': [f"${np.random.randint(2000, 15000):,}" for _ in range(n)], # Грязная строка с $ и запятыми
            'employment_years': np.random.choice([0, 1, 2, 5, 10, '10+', 'missing'], n),
            'credit_history': np.random.choice(['Good', 'Poor', 'Excellent', None], n)
        }
        df = pd.DataFrame(data)
    
        # Добавляем мусор
        df.loc[np.random.choice(n, int(n*0.05)), 'age'] = -10 # Ошибка ввода
    
        if not is_prod:
            # ЗАВИСИМОСТЬ: Вероятность дефолта зависит от возраста (молодые чаще), дохода и истории
            income_num = df['income_usd'].replace(r'[\$,]', '', regex=True).astype(float)
        
            z = -2.0 # Базовый сдвиг (баланс классов - дефолтов всегда меньше)
            z += np.where(df['age'] < 25, 1.5, 0)
            z -= np.where(income_num > 8000, 1.0, 0)
            z += np.where(df['credit_history'] == 'Poor', 2.0, -1.0)
        
            # Сигмоида
            prob_default = 1 / (1 + np.exp(-z))
        
            # Генерируем таргет (1 - дефолт, 0 - вернет)
            df['default'] = np.random.binomial(1, prob_default)
        
        return df

    # Создаем датасеты
    train_df = generate_credit_data(1000, is_prod=False)
    train_df.to_csv('train_credit.csv', index=False)

    prod_df = generate_credit_data(50, is_prod=True)
    prod_df.to_csv('prod_credit.csv', index=False)

    print("Данные для скоринга сгенерированы.")
    # Посмотри на баланс классов в трейне - дефолтов (1) будет гораздо меньше, чем нормальных (0)!
    return (pd,)


@app.cell
def _(pd):
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, f1_score, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    df_train_data = pd.read_csv('train_credit.csv', engine='pyarrow')
    df_prod = pd.read_csv('prod_credit.csv', engine='pyarrow')

    def clean_credit_data(raw_df):
        clean_df = (raw_df
            .assign(
                income_usd = lambda x: x['income_usd']
                    .str.strip()
                    .replace(r'[,$]', '',regex=True)
                    .astype('int64[pyarrow]'),
                employment_years = lambda x: x['employment_years']
                    .str.strip()
                    .replace('10+', '10')
                    .replace('missing', pd.NA)
                    .astype('float64[pyarrow]'),
                employment_years_nan = lambda x: x['employment_years']
                    .isna()
                    .astype('int32[pyarrow]'))
            .assign(
                employment_years = lambda x: x['employment_years']
                    .fillna(x['employment_years'].median())
            )
            .loc[lambda x: x['age'] > 0]
            .dropna(subset=['age', 'income_usd', 'credit_history']))
        return clean_df

    def train_logistic_pipeline(df_clean):
        X = df_clean.drop(columns=['default', 'client_id'])
        y = df_clean['default']

        X_train, X_test, y_train , y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_encoded = pd.get_dummies(X_train, columns=['credit_history'], dtype=int)
        X_test_encoded = pd.get_dummies(X_test, columns=['credit_history'], dtype=int)

        final_columns = X_train_encoded.columns.tolist()
        X_test_encoded = X_test_encoded.reindex(columns=final_columns, fill_value=0)

        scaler = StandardScaler()

        X_train_encoded = scaler.fit_transform(X_train_encoded)
        X_test_encoded = scaler.transform(X_test_encoded)

        model = LogisticRegression(class_weight='balanced', random_state=42)
        model.fit(X=X_train_encoded, y=y_train)

        y_pred_proba = model.predict_proba(X_test_encoded)[:, 1]

        y_pred = (y_pred_proba >= 0.4).astype(int)

        roc = roc_auc_score(y_true=y_test, y_score=y_pred)
        score = f1_score(y_true=y_test, y_pred=y_pred)

        print(f'roc: {roc}, f1: {score}')

        return model, scaler, final_columns
    

    def predict_prod(df_raw, model, scaler, expected_cols):
        df_clean = clean_credit_data(df_raw)

        X_prod = df_clean.drop(columns=['client_id'])

        X_prod_encoded = pd.get_dummies(X_prod, columns=['credit_history'], dtype=int)

        X_prod_encoded = X_prod_encoded.reindex(columns=expected_cols, fill_value=0)

        X_prod_encoded = scaler.transform(X_prod_encoded)

        predictions_proba = model.predict_proba(X_prod_encoded)[:, 1]
    
        predictions = (predictions_proba >= 0.4).astype(int)
        
        result_df = pd.DataFrame({
            'client_id': df_clean['client_id'],
            'probability_default': predictions_proba.round(2),
            'decision': predictions
        }).reset_index(drop=True)

        return result_df


    return (
        clean_credit_data,
        df_prod,
        df_train_data,
        predict_prod,
        train_logistic_pipeline,
    )


@app.cell
def _(
    clean_credit_data,
    df_prod,
    df_train_data,
    predict_prod,
    train_logistic_pipeline,
):
    model, scaler, expected_columns = train_logistic_pipeline(clean_credit_data(df_train_data))

    df_predictions = predict_prod(df_prod, model, scaler, expected_columns)

    df_predictions
    return expected_columns, model


@app.cell
def _(expected_columns, model, pd):
    coef = pd.Series(model.coef_[0], index=expected_columns)
    top_default_features = coef.nlargest(2).index.tolist()
    top_save_features = coef.nsmallest(2).index.tolist()
    print(f'Тянут: {top_default_features}, спасают: {top_save_features}')
    return


if __name__ == "__main__":
    app.run()
