import numpy as np

# 1. Генерируем простые данные (y = 2x + 5 + шум)
np.random.seed(42)
X = np.random.rand(100, 1)
y = 2 * X + 5 + np.random.randn(100, 1) * 0.1

# 2. Инициализируем веса случайными значениями
w = np.random.randn(1, 1)
b = np.random.randn(1)

# Гиперпараметры
learning_rate = 0.1
epochs = 1000  # Сколько раз мы пройдемся по всему датасету
n = len(X)

# 3. Цикл градиентного спуска
for epoch in range(epochs):
    # Прямой проход (Forward pass) - строим предсказание
    y_pred = X * w + b
    
    # Считаем текущую ошибку (MSE)
    loss = np.mean((y - y_pred) ** 2)
    
    # Считаем градиенты (производные)
    dw = - (2 / n) * np.sum(X * (y - y_pred))
    db = - (2 / n) * np.sum(y - y_pred)
    
    # Обновляем веса (делаем шаг вниз)
    w = w - learning_rate * dw
    b = b - learning_rate * db
    
    # Выводим прогресс раз в 100 эпох
    if epoch % 100 == 0:
        print(f"Эпоха {epoch}: Loss = {loss:.4f}, w = {w[0][0]:.4f}, b = {b[0]:.4f}")

print(f"\nФинальные веса модели: w = {w[0][0]:.4f}, b = {b[0]:.4f} (Истинные значения: w=2, b=5)")