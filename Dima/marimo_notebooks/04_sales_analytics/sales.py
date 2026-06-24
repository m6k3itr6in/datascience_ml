import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo
    import pandas as pd
    import numpy as np

    df_sales = pd.read_csv("sales.csv", engine='pyarrow')

    correct_cat = {'apple':'fruits', 'shampoo':'personal_care', 'notebook':'stationery', 'detergent':'household', 'orange_juice':'beverages'}

    def clean_df(raw_df: pd.DataFrame) -> pd.DataFrame:
        df_clean = (
            raw_df
            .rename(columns=lambda x: x.lower().strip())
            .assign(
                sale_id = lambda x: x['sale_id']
                    .astype('int32[pyarrow]'),
                branch = lambda x: x['branch']
                    .str.strip()
                    .str.lower(),
                city = lambda x: x['city']
                    .str.strip()
                    .str.lower()
                    .replace(' ', '_', regex=True),
                customer_type = lambda x: x['customer_type']
                    .str.strip()
                    .str.lower(),
                gender = lambda x: x['gender']
                    .str.strip()
                    .str.lower(),
                product_name = lambda x: x['product_name']
                    .str.strip()
                    .str.lower()
                    .replace(' ', '_', regex=True),
                product_category = lambda x: x['product_name']
                    .map(correct_cat)
                    .astype('string[pyarrow]')
                    .str.strip()
                    .str.lower()
                    .replace(' ', '_', regex=True),
                quantity = lambda x: x['quantity']
                    .astype('int32[pyarrow]'),
                reward_points = lambda x: x['reward_points']
                    .astype('int32[pyarrow]'),
            )
        )
    
        return df_clean

    def find_financial_anomalies(df: pd.DataFrame) -> pd.DataFrame:
        df_anomalies = (
            df
            .loc[:, ['sale_id','unit_price','quantity','tax','total_price']]
            .assign(
                calculated_total = lambda x: round((x['unit_price'] * x['quantity']) + x['tax'], 2),
                is_correct = lambda x: np.isclose(x['total_price'], x['calculated_total'])
            )
            .loc[lambda x: ~x['is_correct']]
        )

        return df_anomalies

    def generate_city_report(df: pd.DataFrame) -> pd.DataFrame:
        report_df = pd.pivot_table(df, index=['city'], columns=['customer_type'], values='total_price', aggfunc='sum', margins=True)

        return report_df


    df_clean = clean_df(df_sales)

    df_clean
    df_fraud = find_financial_anomalies(df_clean)
    len(df_fraud)

    report = generate_city_report(df_clean)
    report
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
