import heapq
import numpy as np
from math import inf

INF = inf

def reduce_cost_matrix(matrix):
    """
    Редукция матрицы: вычитает минимальные элементы строк и столбцов,
    уменьшая стоимость пути.
    Возвращает редуцированную матрицу и суммарную стоимость редукции.
    """
    reduced_matrix = matrix.copy()
    # Редукция по строкам
    row_min = np.min(reduced_matrix, axis=1)
    row_min[np.isinf(row_min)] = 0  # Если минимум равен INF, заменяем на 0
    reduced_matrix -= row_min[:, None]
    
    # Редукция по столбцам
    col_min = np.min(reduced_matrix, axis=0)
    col_min[np.isinf(col_min)] = 0
    reduced_matrix -= col_min
    
    return reduced_matrix, np.sum(row_min) + np.sum(col_min)

def minimum_spanning_tree(matrix, vertices):
    """
    Вычисляет минимальное остовное дерево (MST) для заданного набора вершин с использованием алгоритма Прима.
    Если MST построить невозможно (есть недостижимые вершины), возвращает INF.
    """
    if len(vertices) <= 1:
        return 0.0
    total_cost = 0.0
    visited = set()
    start = next(iter(vertices))
    priority_queue = [(0.0, start)]
    
    while priority_queue:
        weight, u = heapq.heappop(priority_queue)
        if u in visited:
            continue
        total_cost += weight
        visited.add(u)
        for v in vertices - visited:
            edge_weight = matrix[u][v]
            if edge_weight != INF:
                heapq.heappush(priority_queue, (edge_weight, v))
                
    return total_cost if len(visited) == len(vertices) else INF

def tsp_branch_and_bound(matrix, current, visited, current_cost, path, best, selected_edges):
    num_cities = len(matrix)

    if len(visited) == num_cities:
        if matrix[current][0] == INF:
            return
        total_cost = current_cost + matrix[current][0]
        if total_cost < best['cost']:
            best['cost'] = total_cost
            best['path'] = path + [0]
        return

    candidates = [(city, matrix[current][city]) for city in range(num_cities) 
                  if city not in visited and matrix[current][city] != INF]
    candidates.sort(key=lambda x: x[1])

    for next_city, cost_to_next in candidates:
        new_matrix = matrix.copy()
        new_matrix[current, :] = INF  
        new_matrix[:, next_city] = INF  

        # Исключаем преждевременный возврат в начало
        if len(visited) + 1 < num_cities:
            new_matrix[next_city][0] = INF  

        # Определяем, какую дугу нужно запретить
        if current in selected_edges:
            prev_city = selected_edges[current]
            new_matrix[next_city][prev_city] = INF  

        # Запоминаем выбранную дугу
        selected_edges[current] = next_city

        reduced_matrix, reduced_cost = reduce_cost_matrix(new_matrix)
        new_cost = current_cost + cost_to_next + reduced_cost

        remaining_cities = set(range(num_cities)) - visited - {next_city}
        mst_estimate = minimum_spanning_tree(reduced_matrix, remaining_cities) if remaining_cities else 0

        min_edges = []
        for i in remaining_cities:
            row = reduced_matrix[i]
            finite_edges = row[row != INF]
            if finite_edges.size > 0:
                min_edges.append(np.min(finite_edges))
        if len(min_edges) >= 2:
            min_edges_sum = sum(sorted(min_edges)[:2])
        elif len(min_edges) == 1:
            min_edges_sum = min_edges[0]
        else:
            min_edges_sum = 0

        lower_bound = new_cost + min(mst_estimate, min_edges_sum)

        if lower_bound < best['cost']:
            tsp_branch_and_bound(reduced_matrix, next_city, visited | {next_city}, new_cost, path + [next_city], best, selected_edges.copy())

def tsp_little_algorithm(matrix):
    """
    Решает задачу коммивояжера методом Литтла с модификацией.
    Возвращает словарь с ключами 'cost' (стоимость оптимального пути)
    и 'path' (последовательность посещения городов).
    """
    best_solution = {'cost': INF, 'path': []}
    reduced_matrix, initial_cost = reduce_cost_matrix(matrix)
    tsp_branch_and_bound(reduced_matrix, 0, {0}, initial_cost, [0], best_solution, {})
    return best_solution

def tsp_nearest_neighbor(matrix):
    """Жадный алгоритм ближайшего соседа для быстрого, но неоптимального решения задачи коммивояжера."""
    num_cities = len(matrix)
    visited = {0}
    path = [0]
    total_cost = 0
    current_city = 0
    while len(visited) < num_cities:
        next_city = min((i for i in range(num_cities) if i not in visited), key=lambda i: matrix[current_city][i], default=None)
        if next_city is None or matrix[current_city][next_city] == INF:
            return {'cost': INF, 'path': []}  # Нет допустимого маршрута
        visited.add(next_city)
        path.append(next_city)
        total_cost += matrix[current_city][next_city]
        current_city = next_city
    if matrix[current_city][0] == INF:
        return {'cost': INF, 'path': []}  # Не можем вернуться в начало
    path.append(0)
    total_cost += matrix[current_city][0]
    return {'cost': total_cost, 'path': path}

def solve_tsp(matrix, method='little'):
    """Решает задачу коммивояжера с использованием заданного метода (Little или жадного алгоритма)."""
    return tsp_little_algorithm(matrix) if method == 'little' else tsp_nearest_neighbor(matrix)
