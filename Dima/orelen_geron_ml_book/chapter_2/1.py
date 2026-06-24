# Суть в том, что при train_test_split в scikit-learn он разбивает только готовый датасет, а когда приходят новые данные, он их не учитывает и заново их мешает между собой. 
# 
# Поэтому нужно использовать split_train_test_by_id, чтобы учесть новые данные и те которые были в трейне не мешать их в тесте, спросите у нейронки если чет не понятно

import numpy as np
import pandas as pd

day1_data = [
    {"order_id": 101, "distance_km": "12.5", "predicted_hours": 1.5, "actual_hours": 1.8},
    {"order_id": 102, "distance_km": "45.0", "predicted_hours": 4.0, "actual_hours": 3.9},
    {"order_id": 103, "distance_km": "5.2", "predicted_hours": 0.8, "actual_hours": None}, # Пропуск
    {"order_id": 104, "distance_km": "120.0", "predicted_hours": 10.0, "actual_hours": 11.2},
    {"order_id": 105, "distance_km": "3.1", "predicted_hours": 0.5, "actual_hours": "0.6"}, 
    {"order_id": 106, "distance_km": "15.0", "predicted_hours": 2.0, "actual_hours": 48.0}, # Выброс
    {"order_id": 107, "distance_km": "missing", "predicted_hours": 3.0, "actual_hours": 3.2}, 
]

day2_data = day1_data + [
    {"order_id": 108, "distance_km": "8.4", "predicted_hours": 1.1, "actual_hours": 1.2},
    {"order_id": 109, "distance_km": "22.1", "predicted_hours": 2.5, "actual_hours": 2.7},
    {"order_id": 110, "distance_km": "60.0", "predicted_hours": 5.0, "actual_hours": None}, # Снова пропуск
]

def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

from zlib import crc32

def test_set_check(identifier, test_ratio):
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

def split_train_test_by_id(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]

def clean_data(df):
    clean_df = (df
        .assign(
            distance_km = lambda x: pd.to_numeric(x['distance_km'], errors='coerce')
                .astype('float64[pyarrow]'),
            actual_hours = lambda x: pd.to_numeric(x['actual_hours'], errors='coerce')
                .astype('float64[pyarrow]')
        )
    ).dropna(subset=['distance_km', 'actual_hours']).reset_index(drop=True)
    return clean_df

def calculate_rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def calculate_mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

if __name__ == "__main__":
    day1_df = pd.DataFrame(day1_data)
    day2_df = pd.DataFrame(day2_data)
    
    clean_day_1_df = clean_data(day1_df)
    clean_day_2_df = clean_data(day2_df)

    # Разделение на Train/Test по ID для обоих дней
    train_day1, test_day1 = split_train_test_by_id(clean_day_1_df, 0.2, 'order_id')
    train_day2, test_day2 = split_train_test_by_id(clean_day_2_df, 0.2, 'order_id')

    # Проверка, что ID из трейна первого дня не утекли в тест второго дня
    assert not any(train_day1['order_id'].isin(test_day2['order_id'])), "ID leakage detected!"

    # RMSE и MAE для всего test2 (с выбросом 106)
    rmse_with_106 = calculate_rmse(test_day2['actual_hours'], test_day2['predicted_hours'])
    mae_with_106 = calculate_mae(test_day2['actual_hours'], test_day2['predicted_hours'])

    # RMSE и MAE для test2 без заказа 106
    test_day2_no_106 = test_day2.loc[lambda x: x['order_id'] != 106]
    rmse_without_106 = calculate_rmse(test_day2_no_106['actual_hours'], test_day2_no_106['predicted_hours'])
    mae_without_106 = calculate_mae(test_day2_no_106['actual_hours'], test_day2_no_106['predicted_hours'])

    # Вывод результатов
    print(f"RMSE (with 106): {rmse_with_106:.4f}")
    print(f"MAE (with 106): {mae_with_106:.4f}")
    print(f"RMSE (without 106): {rmse_without_106:.4f}")
    print(f"MAE (without 106): {mae_without_106:.4f}")