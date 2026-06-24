import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    return np, pd


@app.cell
def _(np):
    dirty_crm_data = {
        "CLIENT ID":[" 1001", "1002", "1003", "1001 ", "1004", "1005", "1006"],
        "FULL_Name":["John Doe", "JANE SMITH", "  Michael jordan", "John Doe", "chris evans", "N/A", "Bruce Wayne"],
        "Account_Balance":["$1,250.50", "$500.00", "$-200.0", "$1,250.50", "MISSING", "$0.0", "$9999.99"],
        "Status":["Active", "active", "Suspended", "Active", "Inactive", "Active", "active"],
        "Last_Login_Days_Ago":[5, 12, np.nan, 5, 120, 2, np.nan]
    }
    return (dirty_crm_data,)


@app.cell
def _(dirty_crm_data, pd):
    df_clean = (
        pd.DataFrame(data=dirty_crm_data)
            .rename(
                columns=lambda x: 
                    x.lower().replace(' ', '_')
            )
            .assign(
                client_id=lambda x: x['client_id']
                    .str
                    .strip()
                    .astype('int32[pyarrow]'))
            .drop_duplicates(subset=['client_id'])
            .assign(
                full_name=lambda x: x['full_name']
                    .str
                    .strip()
                    .str
                    .title()
                    .astype('string[pyarrow]')
            )
            .loc[lambda x: x['full_name'] != 'N/A']
            .assign(
                status=lambda x: x['status']
                    .str
                    .title()
                    .astype('string[pyarrow]')
            )
            .assign(
                account_balance=lambda x: x['account_balance']
                    .replace('MISSING', pd.NA)
                    .replace(r'[\$,]', '', regex=True)
                    .astype('float64[pyarrow]')
            )
    )

    df_clean
    return (df_clean,)


@app.cell
def _(df_clean):
    df_clean.loc[lambda x: x['status'] == 'Suspended', 'account_balance'] = 0.0

    df_clean
    return


@app.cell
def _(df_clean):
    df_final = df_clean.loc[
        lambda x: 
            (x['status'] == 'Active') & (x['account_balance'] >= 0), 
        ['client_id', 'account_balance']].sort_values(
            by='account_balance', ascending=False
        )

    df_final
    return


@app.cell
def _():
    dirty_audit_log =[
        {"  TxN_ID ": " TX-1001 ", "Cust_Name": " LeBron james ", " amount ": "$1,250.50", " DATE ": "2026-03-25", "Status": "COMPLETED"},
        {"  TxN_ID ": "TX-1002", "Cust_Name": "stephen curry", " amount ": "$890.00", " DATE ": "2026-03-26", "Status": " pending "},
        {"  TxN_ID ": "TX-1001 ", "Cust_Name": " LeBron james ", " amount ": "$1,250.50", " DATE ": "2026-03-25", "Status": "COMPLETED"}, # Дубликат!
        {"  TxN_ID ": "TX-1003", "Cust_Name": " Kevin Durant ", " amount ": "ERROR", " DATE ": "N/A", "Status": "FAILED"},
        {"  TxN_ID ": "TX-1004", "Cust_Name": "N/A", " amount ": "$45.00", " DATE ": "2026-03-28", "Status": "COMPLETED"},
        {"  TxN_ID ": "TX-1005", "Cust_Name": "Luka Doncic", " amount ": "$12,500.00", " DATE ": "2026-03-29", "Status": "completed"}
    ]
    return (dirty_audit_log,)


@app.cell
def _(dirty_audit_log, pd):
    df_clean_audit_log = (
        pd.DataFrame(data=dirty_audit_log)
            .rename(
                columns=lambda x: x
                    .lower()
                    .strip()
            )
            .astype('string[pyarrow]')
            .assign(
                txn_id=lambda x: x['txn_id']
                    .str
                    .strip(),
                amount=lambda x: x['amount']
                    .replace(r'[\$,]', '', regex=True)
                    .replace('ERROR', pd.NA)
                    .astype('float64[pyarrow]'),
                cust_name=lambda x: x['cust_name']
                    .str
                    .title()
                    .str
                    .strip()
                    .replace('N/A', pd.NA),
                status=lambda x: x['status']
                    .str
                    .upper()
                    .str
                    .strip(),
                date=lambda x: x['date']
                    .replace('N/A', pd.NA)
                    .astype('date64[pyarrow]')
            )
            .drop_duplicates(subset=['txn_id'])
            .loc[lambda x: (x['status'] != 'FAILED') & (x['amount'].notna())]
            .fillna({'cust_name':'Unknown'})
            .sort_values('amount', ascending=False)
            .head(3)
            .loc[:, ['txn_id', 'cust_name', 'amount']]
    )

    df_clean_audit_log
    return


@app.cell
def _():
    dirty_payroll =[
        {"  Emp_ID  ": "EMP-001", "FullName_Dept": " luke skywalker | SALES ", " Base_Salary ": "$7,500.50", "Bonus_Mult": "1.5x", "Date ": "25-03-2026"},
        {"  Emp_ID  ": " emp_002", "FullName_Dept": "leia organa|hr", " Base_Salary ": "8,200.00", "Bonus_Mult": "None", "Date ": "2026/03/26"},
        {"  Emp_ID  ": "003 ", "FullName_Dept": " han solo | Logistics ", " Base_Salary ": "$5,400.00", "Bonus_Mult": "2.0 X", "Date ": "27-03-2026"},
        {"  Emp_ID  ": "EMP-001", "FullName_Dept": " luke skywalker | SALES ", " Base_Salary ": "$7,500.50", "Bonus_Mult": "1.5x", "Date ": "25-03-2026"}, # Дубликат!
        {"  Emp_ID  ": "EMP-004", "FullName_Dept": " darth vader | management ", " Base_Salary ": "ERROR", "Bonus_Mult": "3.0x", "Date ": "N/A"},
        {"  Emp_ID  ": "EMP-005", "FullName_Dept": " yoda | SALES ", " Base_Salary ": "$9,000.00", "Bonus_Mult": "1.0x", "Date ": "2026/03/29"}
    ]
    return (dirty_payroll,)


@app.cell
def _(dirty_payroll, pd):
    df_clean_payroll = (
        pd.DataFrame(data=dirty_payroll)
            .rename(columns=lambda x:x.lower().strip())
            .astype('string[pyarrow]')
            .assign(
                emp_id=lambda x:x['emp_id']
                    .str.lower()
                    .str.strip()
                    .replace('_', '-', regex=True)
                    .replace('emp-', '', regex=True)
                    .astype('int32[pyarrow]'),
                employee_name=lambda x:x['fullname_dept']
                    .str.split('|')
                    .str[0]
                    .str.strip()
                    .str.title()
                    .astype('string[pyarrow]'),
                department=lambda x:x['fullname_dept']
                    .str.split('|')
                    .str[1]
                    .str.strip()
                    .str.upper()
                    .astype('string[pyarrow]'),
                base_salary=lambda x:x['base_salary']
                    .str.strip()
                    .replace(r'[\$,]', '', regex=True)
                    .replace('ERROR', pd.NA)
                    .astype('float64[pyarrow]'),
                bonus_mult=lambda x:x['bonus_mult']
                    .replace(r'[xX]', '', regex=True)
                    .str.strip()
                    .replace('None', '1.0')
                    .astype('float64[pyarrow]'),
                total_pay=lambda x:x['base_salary'] * x['bonus_mult'],
                date=lambda x:pd.to_datetime(
                    x['date']
                    .replace('N/A', pd.NaT),
                    dayfirst=True,
                    format='mixed',
                    errors='coerce'
                    )
                    .astype('timestamp[ns][pyarrow]')

            )
            .drop(columns=['fullname_dept'])
            .drop_duplicates(subset=['emp_id'])
            .loc[lambda x: (x['department'] != 'HR') & (x['total_pay'].notna())]
            .sort_values('total_pay', ascending=False)
            .head(3)
            .loc[:, ['emp_id', 'employee_name', 'department', 'total_pay']]
    )

    df_clean_payroll
    return


@app.cell
def _(dirty_payroll, pd):
    ## создание функций, а не просто разового скрипта обработки данных
    def clean_payroll_data(raw_data: list[dict]) -> pd.DataFrame:
        df_clean = (
            pd.DataFrame(data=raw_data)
                .rename(columns=lambda x:x.lower().strip())
                .astype('string[pyarrow]')
                .assign(
                    emp_id=lambda x:x['emp_id']
                        .str.lower()
                        .str.strip()
                        .replace('_', '-', regex=True)
                        .replace('emp-', '', regex=True)
                        .astype('int32[pyarrow]'),
                    employee_name=lambda x:x['fullname_dept']
                        .str.split('|')
                        .str[0]
                        .str.strip()
                        .str.title()
                        .astype('string[pyarrow]'),
                    department=lambda x:x['fullname_dept']
                        .str.split('|')
                        .str[1]
                        .str.strip()
                        .str.upper()
                        .astype('string[pyarrow]'),
                    base_salary=lambda x:x['base_salary']
                        .str.strip()
                        .replace(r'[\$,]', '', regex=True)
                        .replace('ERROR', pd.NA)
                        .astype('float64[pyarrow]'),
                    bonus_mult=lambda x:x['bonus_mult']
                        .replace(r'[xX]', '', regex=True)
                        .str.strip()
                        .replace('None', '1.0')
                        .astype('float64[pyarrow]'),
                    total_pay=lambda x:x['base_salary'] * x['bonus_mult'],
                    date=lambda x:pd.to_datetime(
                        x['date']
                        .replace('N/A', pd.NaT),
                        dayfirst=True,
                        format='mixed',
                        errors='coerce'
                        )
                        .astype('timestamp[ns][pyarrow]')

                    )
            .drop(columns=['fullname_dept'])
            .drop_duplicates(subset=['emp_id'])
        )
        return df_clean

    def get_top_paid_employees(clean_df: pd.DataFrame, top_n: int = 3, exclude_dept: str = 'HR') -> pd.DataFrame:
        df_report = (
            clean_df
            .loc[lambda x: (x['department'] != exclude_dept) & (x['total_pay'].notna())]
            .sort_values('total_pay', ascending=False)
            .head(top_n)
            .loc[:, ['emp_id', 'employee_name', 'department', 'total_pay']]
        )

        return df_report

    base_payroll_df = clean_payroll_data(dirty_payroll)
    final_report_df = get_top_paid_employees(base_payroll_df, top_n=3, exclude_dept='HR')

    final_report_df
    return


if __name__ == "__main__":
    app.run()
