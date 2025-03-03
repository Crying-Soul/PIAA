import time
import numpy as np
import matplotlib.pyplot as plt
from tsp_algorithms import solve_tsp
from utils import generate_matrix

def benchmark_tsp(matrix_sizes, runs=5):
    """Запускает тестирование методов решения задачи коммивояжера для матриц разного размера и строит таблицу результатов.
    
    Аргументы:
    matrix_sizes -- список размеров матриц для тестирования (list[int])
    runs -- количество запусков для каждого размера матрицы (int, по умолчанию 5)
    
    Действия:
    1. Для каждого размера матрицы генерируется случайная матрица.
    2. Для каждого метода ('little' и 'nearest') вычисляется средняя стоимость пути и время выполнения.
    3. Результаты выводятся в виде таблицы.
    4. Строится график зависимости времени выполнения от размера матрицы для обоих методов.
    """
    methods = ['little', 'nearest']
    results = []
    little_times = []
    nearest_times = []
    
    for size in matrix_sizes:
        matrix = generate_matrix(size, seed=99)
        matrix_np = np.array(matrix)
        row = [size]
        
        avg_costs = {}
        avg_times = {}
        
        for method in methods:
            total_cost, total_time = 0, 0
            
            for _ in range(runs):
                start_time = time.time()
                best_solution = solve_tsp(matrix_np, method)
                end_time = time.time()
                total_cost += best_solution['cost']
                total_time += (end_time - start_time)
            
            avg_cost = total_cost / runs
            avg_time = total_time / runs
            avg_costs[method] = avg_cost
            avg_times[method] = avg_time
            row.extend([avg_cost, avg_time])
            
            if method == 'little':
                little_times.append(avg_time)
            elif method == 'nearest':
                nearest_times.append(avg_time)
        
        deviation = ((avg_costs['nearest'] - avg_costs['little']) / avg_costs['little']) * 100 if avg_costs['little'] != 0 else float('inf')
        row.append(deviation)
        
        results.append(row)
    
    print("\nРезультаты бенчмарка:\n")
    print(f"{'Размер':<10}{'Little Cost':<15}{'Little Time':<15}{'Nearest Cost':<15}{'Nearest Time':<15}{'Deviation (%)':<15}")
    print("-" * 85)
    for row in results:
        print(f"{row[0]:<10}{row[1]:<15.2f}{row[2]:<15.4f}{row[3]:<15.2f}{row[4]:<15.4f}{row[5]:<15.2f}")
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(matrix_sizes, little_times, label='Little Method', marker='o')
    plt.plot(matrix_sizes, nearest_times, label='Nearest Method', marker='o')
    plt.xlabel('Размер матрицы')
    plt.ylabel('Время (секунды)')
    plt.title('Время работы алгоритмов в зависимости от размера матрицы')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    benchmark_tsp([i for i in range(4, 19)])