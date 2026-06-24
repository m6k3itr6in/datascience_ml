import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    # Приходит из API каждую ночь
    raw_api_response =[
        {"order_id": "A-001", "category": "Electronics", "price": "1500.50", "currency": "USD"},
        {"order_id": "A-002", "category": "Furniture", "price": "300.00", "currency": "EUR"},
        {"order_id": "A-003", "category": "Electronics"}, # Внезапно API не прислал цену!
        {"order_id": "A-004", "category": "Books", "price": "15.99", "currency": "USD"},
        {"order_id": "A-005", "category": "Furniture", "price": "system_error", "currency": "USD"} # Сбой на фронтенде!
    ]

    # Код джуна (работает прямо в глобальной области видимости):
    # df = pd.DataFrame(raw_api_response)
    # df['price'] = df['price'].fillna('0')
    # df['price'] = df['price'].str.replace('$', '')

    # # СКРИПТ ПАДАЕТ ТУТ: ValueError: could not convert string to float: 'system_error'
    # df['price'] = df['price'].astype(float) 

    # df['currency'] = df['currency'].fillna('USD')
    # res = df.groupby('category')['price'].sum()
    # print("Отчет готов:")
    # print(res)

    def clean_orders_data(raw_data: list[dict]) -> pd.DataFrame:
        """Очистка данных"""
    
        df = pd.DataFrame(raw_data)
    
        clean_df = (
            df
            .rename(columns=lambda x: x.lower().strip())
            .assign(
                order_id = lambda x: x['order_id']
                    .replace(r'^.*-', '', regex=True)
                    .astype('int32[pyarrow]'),
                category = lambda x: x['category']
                    .astype('string[pyarrow]'),
                price = lambda x: pd.to_numeric(x['price'], errors='coerce')
                    .astype('float64[pyarrow]'),
                currency = lambda x: x['currency']
                    .fillna('USD')
                    .astype('string[pyarrow]')
                    .str.strip()
            )
            .dropna(subset=['price'])
        )
    
        return clean_df

    def generate_revenue_report(df_for_report: pd.DataFrame) -> pd.DataFrame:
        """Вывод отчета"""
        try:
            df_report = (
                df_for_report
                .groupby(['category', 'currency'])[['price']].sum()
            )

            return df_report
        
        except KeyError:
            print('Отсутствует необходимая колонка')

            return pd.DataFrame()


    if __name__ == '__main__':
        clean_df = clean_orders_data(raw_api_response)

        report = generate_revenue_report(clean_df)
        print(report)
    return


if __name__ == "__main__":
    app.run()
