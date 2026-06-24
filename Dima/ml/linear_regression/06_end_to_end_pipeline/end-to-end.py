import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression, Lasso
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    # Фиксируем seed для воспроизводимости
    np.random.seed(42)

    # 1. Генерируем исторические данные (Трейн)
    n_train = 500
    train_data = {
        'id': range(1, n_train + 1),
        'area_sqm': [f"{np.random.randint(20, 150)} sq.m." if np.random.rand() > 0.1 else f"{np.random.randint(20, 150)} м2" for _ in range(n_train)],
        'rooms': np.random.choice(['1', '2', '3', '4', 'five', 'Студия', None], n_train, p=[0.3, 0.3, 0.2, 0.05, 0.05, 0.05, 0.05]),
        'district': np.random.choice(['Center', 'center', 'North', 'north ', 'South', 'East', 'UNKNOWN'], n_train),
        'has_balcony': np.random.choice(['yes', 'no', '1', '0', None], n_train),
        'price': np.random.normal(5000000, 1500000, n_train) # Целевая переменная
    }
    df_train = pd.DataFrame(train_data)
    # Добавляем немного дичи в цены (выбросы и NaN)
    df_train.loc[10:15, 'price'] = np.nan
    df_train.loc[100:105, 'price'] = 999999999 

    df_train.to_csv('train_dirty_houses.csv', index=False)

    # 2. Генерируем новые данные (Прод/Инференс) - ЦЕН НЕТ!
    n_prod = 50
    prod_data = {
        'id': range(1001, 1001 + n_prod),
        'area_sqm': [f"{np.random.randint(30, 120)} кв.м" for _ in range(n_prod)], # Опа, новый формат!
        'rooms': np.random.choice(['1', '2', '3', None], n_prod),
        'district': np.random.choice(['Center', 'North', 'West'], n_prod), # Появился West, которого не было в трейне!
        'has_balcony': np.random.choice(['yes', 'no'], n_prod),
    }
    df_prod = pd.DataFrame(prod_data)
    df_prod.to_csv('prod_new_houses.csv', index=False)

    print("Дерьмовые данные успешно сгенерированы. Удачи.")
    return (
        Lasso,
        StandardScaler,
        mean_absolute_error,
        pd,
        r2_score,
        train_test_split,
    )


@app.cell
def _(
    Lasso,
    StandardScaler,
    mean_absolute_error,
    pd,
    r2_score,
    train_test_split,
):
    df_train_dirty_houses = pd.read_csv('train_dirty_houses.csv', dtype_backend='pyarrow')

    df_prod_new_houses = pd.read_csv('prod_new_houses.csv', dtype_backend='pyarrow')

    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        dropna_cols = ['rooms', 'district', 'has_balcony']
        if 'price' in df.columns:
            dropna_cols.append('price')
    
        clean_df = (df
            .assign(
                area_sqm = lambda x: x['area_sqm']
                    .str.extract(r'(?P<area>\d+)', expand=False)
                    .astype('int32[pyarrow]'),
                rooms = lambda x: x['rooms']
                    .replace(r'^\s*$', pd.NA, regex=True)
                    .replace('Студия', '0')
                    .replace('five', '5')
                    .astype('int32[pyarrow]'),
                district = lambda x: x['district']
                    .str.lower()
                    .str.strip()
                    .replace('unknown', pd.NA),
                has_balcony = lambda x: x['has_balcony']
                    .str.lower()
                    .str.strip()
                    .replace({'1': 'yes', '0': 'no', '': pd.NA})
            )
        )
    
        if 'price' in df.columns:
            clean_df = clean_df.assign(price = lambda x: x['price'].round(2))
        
        clean_df = clean_df.dropna(subset=dropna_cols)
    
        if 'price' in df.columns:
            clean_df = clean_df.loc[lambda x: x['price'] < 100000000]

        return clean_df

    def train_pipeline(df_clean: pd.DataFrame) -> tuple:
        if 'price' not in df_clean.columns:
            raise ValueError("нет цены")
    
        X = df_clean.drop(columns=['price', 'id'])
        y = df_clean['price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        cat_cols = ['district', 'has_balcony']
        X_train_encoded = pd.get_dummies(X_train, columns=cat_cols, dtype=int)
        X_test_encoded = pd.get_dummies(X_test, columns=cat_cols, dtype=int)

        final_columns = X_train_encoded.columns.tolist()
        X_test_encoded = X_test_encoded.reindex(columns=final_columns, fill_value=0)

        num_cols = ['area_sqm', 'rooms']
        scaler = StandardScaler()

        X_train_encoded[num_cols] = scaler.fit_transform(X_train_encoded[num_cols])
        X_test_encoded[num_cols] = scaler.transform(X_test_encoded[num_cols])

        model = Lasso(alpha=0.1, random_state=42, max_iter=10000)
        model.fit(X=X_train_encoded, y=y_train)

        y_pred = model.predict(X_test_encoded)
        mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)
        r2 = r2_score(y_true=y_test, y_pred=y_pred)

        print(f"mae: {mae:.2f}, r2: {r2:.4f}")
    
        return model, scaler, final_columns

    def predict_prod(df_raw: pd.DataFrame, model, scaler, expected_columns: list) -> pd.DataFrame:
        df_clean = clean_data(df_raw)

        X_prod = df_clean.drop(columns=['id'])

        cat_cols = ['district', 'has_balcony']
        X_prod_encoded = pd.get_dummies(X_prod, columns=cat_cols, dtype=int)

        X_prod_encoded = X_prod_encoded.reindex(columns=expected_columns, fill_value=0)

        num_cols = ['area_sqm', 'rooms']
        X_prod_encoded[num_cols] = scaler.transform(X_prod_encoded[num_cols])

        predictions = model.predict(X_prod_encoded)

        result_df = pd.DataFrame({
            'id': df_clean['id'],
            'price': predictions.round(2)
        }).reset_index(drop=True)

        return result_df

    return (
        clean_data,
        df_prod_new_houses,
        df_train_dirty_houses,
        predict_prod,
        train_pipeline,
    )


@app.cell
def _(
    clean_data,
    df_prod_new_houses,
    df_train_dirty_houses,
    predict_prod,
    train_pipeline,
):
    model, scaler, expected_columns = train_pipeline(clean_data(df_train_dirty_houses))

    df_predictions = predict_prod(df_prod_new_houses, model, scaler, expected_columns)

    print(df_predictions.head())
    return


if __name__ == "__main__":
    app.run()
