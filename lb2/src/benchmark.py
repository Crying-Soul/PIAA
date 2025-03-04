import time
import numpy as np
import matplotlib.pyplot as plt
from tsp_algorithms import solve_tsp
from utils import generate_matrix
from concurrent.futures import ProcessPoolExecutor

def run_tsp_method(matrix, method, runs):
    """Запуск метода решения задачи коммивояжера для одного метода и одной матрицы."""
    total_cost, total_time = 0, 0
    start_time = time.time()
    for _ in range(runs):
        best_solution = solve_tsp(matrix, method)
        total_cost += best_solution['cost']
    total_time = time.time() - start_time
    avg_cost = total_cost / runs
    avg_time = total_time / runs
    return avg_cost, avg_time

def benchmark_tsp(matrix_sizes, runs=10):
    """Запускает тестирование методов решения задачи коммивояжера для матриц разного размера и строит таблицу результатов."""
    start_time_bench = time.time()
    methods = ['little', 'nearest']
    results = []
    little_times = []
    nearest_times = []
    little_costs = []
    nearest_costs = []
    
    # Предварительная генерация всех матриц
    matrices = {size: generate_matrix(size, seed=52) for size in matrix_sizes}
    
    with ProcessPoolExecutor() as executor:
        for size in matrix_sizes:
            matrix = matrices[size]
            row = [size]
            
            # Запуск методов в многозадачном режиме
            futures = {method: executor.submit(run_tsp_method, matrix, method, runs) for method in methods}
            avg_costs = {}
            avg_times = {}
            
            for method in methods:
                avg_cost, avg_time = futures[method].result()
                avg_costs[method] = avg_cost
                avg_times[method] = avg_time
                row.extend([avg_cost, avg_time])
                
                if method == 'little':
                    little_times.append(avg_time)
                    little_costs.append(avg_cost)
                elif method == 'nearest':
                    nearest_times.append(avg_time)
                    nearest_costs.append(avg_cost)
            
            # Расчет отклонения
            deviation = ((avg_costs['nearest'] - avg_costs['little']) / avg_costs['little']) * 100 if avg_costs['little'] != 0 else float('inf')
            row.append(deviation)
            results.append(row)
    
    # Вывод результатов
    print("\nРезультаты бенчмарка:\n")
    print(f"{'Размер':<10}{'Little Cost':<15}{'Little Time':<15}{'Nearest Cost':<15}{'Nearest Time':<15}{'Deviation (%)':<15}")
    print("-" * 85)
    for row in results:
        print(f"{row[0]:<10}{row[1]:<15.2f}{row[2]:<15.4f}{row[3]:<15.2f}{row[4]:<15.4f}{row[5]:<15.2f}")
    
    end_time_bench = time.time()
    print(f"Время выполнения бенчмарка: {end_time_bench - start_time_bench:.4f} секунд\n")
    
    # Построение графиков
    fig, axs = plt.subplots(2, 1, figsize=(10, 12))
    
    # График времени
    axs[0].plot(matrix_sizes, little_times, label='Little Method', marker='o')
    axs[0].plot(matrix_sizes, nearest_times, label='Nearest Method', marker='o')
    axs[0].set_xlabel('Размер матрицы')
    axs[0].set_ylabel('Время (секунды)')
    axs[0].set_title('Время работы алгоритмов в зависимости от размера матрицы')
    axs[0].legend()
    axs[0].grid(True)
    
    # График стоимости
    axs[1].plot(matrix_sizes, little_costs, label='Little Method', marker='o')
    axs[1].plot(matrix_sizes, nearest_costs, label='Nearest Method', marker='o')
    axs[1].set_xlabel('Размер матрицы')
    axs[1].set_ylabel('Стоимость (единицы)')
    axs[1].set_title('Сравнение стоимости решений для алгоритмов')
    axs[1].legend()
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    benchmark_tsp([i for i in range(4, 21, 2)])
