import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    np.random.seed(42)

    def generate_telecom_data(n, is_prod=False):
        data = {
            'client_id': range(1000, 1000 + n) if not is_prod else range(9000, 9000 + n),
            'monthly_charges': np.random.uniform(10, 120, n),
            'tenure_months': np.random.randint(0, 72, n),
            'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year', ' 1 yr', 'monthly'], n),
            'tech_support': np.random.choice(['Yes', 'No', 'No internet service', pd.NA], n),
        }
        df = pd.DataFrame(data)

        # Добавляем мусор
        df.loc[np.random.choice(n, int(n*0.05)), 'monthly_charges'] = -999 # Ошибка БД
        df['tenure_months'] = df['tenure_months'].astype(str)
        df.loc[np.random.choice(n, int(n*0.05)), 'tenure_months'] = 'N/A'

        if not is_prod:
            # Уходят те, у кого Month-to-month контракт, высокие платежи и нет техподдержки
            prob_churn = np.zeros(n)
            prob_churn += np.where(df['contract_type'].isin(['Month-to-month', 'monthly']), 0.4, 0.0)
            prob_churn += np.where(df['monthly_charges'] > 80, 0.3, 0.0)
            prob_churn += np.where(df['tech_support'] == 'No', 0.2, 0.0)
            prob_churn = np.clip(prob_churn, 0, 1)

            df['churn'] = np.random.binomial(1, prob_churn)

        return df

    train_df = generate_telecom_data(800, is_prod=False)
    train_df.to_csv('train_telecom.csv', index=False)

    prod_df = generate_telecom_data(100, is_prod=True)
    prod_df.to_csv('prod_telecom.csv', index=False)

    print("Данные телекома сгенерированы!")
    return np, pd


@app.cell
def _(np, pd):
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import f1_score, roc_auc_score

    df_prod_telecom = pd.read_csv('prod_telecom.csv', engine='pyarrow')

    df_train_telecom = pd.read_csv('train_telecom.csv', engine='pyarrow')

    contract_map = {
        '1_yr': 'one_year',
        'month-to-month': 'monthly'
    }

    def clean_telecom_data(df: pd.DataFrame) -> pd.DataFrame:
        df_clean = (df
            .assign(
                monthly_charges = lambda x: x['monthly_charges']
                    .replace(-999, pd.NA)
                    .astype('float[pyarrow]'),
                tenure_months = lambda x: x['tenure_months']
                    .replace('N/A', pd.NA),
                contract_type = lambda x: x['contract_type']
                    .str.strip()
                    .str.lower()
                    .replace(' ', '_', regex=True)
                    .replace(contract_map),
                tech_support = lambda x: x['tech_support']
                    .str.strip()
                    .str.lower()
                    .replace(' ', '_', regex=True)
                    .replace(pd.NA, 'unknown')
            )
            .assign(
                monthly_charges = lambda x: x['monthly_charges']
                    .fillna(x['monthly_charges'].median()),
                tenure_months = lambda x: x['tenure_months']
                    .fillna(x['tenure_months'].median()),
            )
        )

        return df_clean

    def train_tree_pipeline(df_clean: pd.DataFrame) -> tuple:
        X = df_clean.drop(columns=['client_id', 'churn'])
        y = df_clean['churn']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        cat_columns = ['contract_type', 'tech_support']
        X_train_encoded = pd.get_dummies(X_train, columns=cat_columns, dtype=int)
        X_test_encoded = pd.get_dummies(X_test, columns=cat_columns, dtype=int)

        final_columns = X_train_encoded.columns.tolist()
        X_test_encoded = X_test_encoded.reindex(columns=final_columns, fill_value=0)

        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, class_weight='balanced')
        model.fit(X=X_train_encoded, y=y_train)

        y_pred = model.predict(X_test_encoded)
        y_pred_proba = model.predict_proba(X_test_encoded)[:, 1]

        score = f1_score(y_true=y_test, y_pred=y_pred)
        roc_auc = roc_auc_score(y_true=y_test, y_score=y_pred_proba)

        print(f'f1_score: {score:.2f}, roc_auc: {roc_auc:.2f}')

        best_threshold = 0.5
        best_f1 = 0.0

        for threshold in np.arange(0.1, 0.9, 0.05):
            y_pred_temp = (y_pred_proba >= threshold).astype(int)
            score_temp = f1_score(y_test, y_pred_temp)

            if score_temp > best_f1:
                best_f1 = score_temp
                best_threshold = threshold

        print(f'Лучший порог: {best_threshold:.2f} с F1: {best_f1:.2f}')

        return model, final_columns, best_threshold

    def predict_telecom_prod(df_raw, model, expected_cols, best_threshold) -> pd.DataFrame:
        df_clean = clean_telecom_data(df_raw)

        X_prod = df_clean.drop(columns=['client_id'])

        cat_columns = ['contract_type', 'tech_support']
        X_prod_encoded = pd.get_dummies(X_prod, columns=cat_columns, dtype=int)

        X_prod_encoded = X_prod_encoded.reindex(columns=expected_cols, fill_value=0)

        proba = model.predict_proba(X_prod_encoded)[:, 1]

        predictions = (proba >= best_threshold).astype(int)

        result_df = pd.DataFrame({
            'id': df_clean['client_id'],
            'proba': proba,
            'churn': predictions
        }).reset_index(drop=True)

        return result_df

    model, expected_columns, best_threshold = train_tree_pipeline(clean_telecom_data(df_train_telecom))

    df_predictions = predict_telecom_prod(df_prod_telecom, model, expected_columns, best_threshold)

    df_predictions.round(2)
    return


if __name__ == "__main__":
    app.run()
