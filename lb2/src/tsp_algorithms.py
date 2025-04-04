import heapq
import numpy as np
from math import inf

def reduce_cost_matrix(matrix, verbose=False):
    """Редуцирует матрицу затрат, вычитая минимальные значения строк и столбцов.
    
    Аргументы:
    matrix -- матрица затрат (numpy.ndarray)
    verbose -- флаг для вывода промежуточных результатов (bool, по умолчанию False)
    
    Возвращает:
    reduced_matrix -- редуцированная матрица (numpy.ndarray)
    total_reduction -- сумма всех вычтенных минимумов (float)
    """
    reduced_matrix = matrix.copy()
    row_min = np.min(reduced_matrix, axis=1)
    row_min[np.isinf(row_min)] = 0
    reduced_matrix -= row_min[:, None]
    
    col_min = np.min(reduced_matrix, axis=0)
    col_min[np.isinf(col_min)] = 0
    reduced_matrix -= col_min
    
    if verbose:
        print("=== Редукция матрицы ===")
        print(f"Минимумы строк: {row_min}")
        print(f"Минимумы столбцов: {col_min}")
        print(f"Нижняя граница: {np.sum(row_min) + np.sum(col_min)}")
        print(f"Редуцированная матрица:\n{reduced_matrix}")
        
    
    return reduced_matrix, np.sum(row_min) + np.sum(col_min)

def minimum_spanning_tree(matrix, vertices, verbose=False):
    """Вычисляет минимальное остовное дерево (MST) для заданного множества вершин.
    
    Аргументы:
    matrix -- матрица затрат (numpy.ndarray)
    vertices -- множество вершин (set)
    verbose -- флаг для вывода промежуточных результатов (bool, по умолчанию False)
    
    Возвращает:
    total_cost -- стоимость минимального остовного дерева (float)
    """
    if len(vertices) <= 1:
        return 0.0
    total_cost = 0.0
    visited = set()
    start = next(iter(vertices))
    priority_queue = [(0.0, start)]
    
    if verbose:
        print(f"=== Вычисление MST для вершин {vertices} ===")
    
    while priority_queue:
        weight, u = heapq.heappop(priority_queue)
        if u in visited:
            continue
        total_cost += weight
        visited.add(u)
        for v in vertices - visited:
            edge_weight = matrix[u][v]
            if edge_weight != inf:
                heapq.heappush(priority_queue, (edge_weight, v))
                if verbose:
                    print(f"Добавлено ребро {u} -> {v} с весом {edge_weight}")
    
    if verbose:
        print(f"MST оценка оставшихся вершин: {total_cost}")
    
    return total_cost if len(visited) == len(vertices) else inf

def tsp_branch_and_bound(matrix, current, visited, current_cost, path, best, selected_edges, verbose=False, depth=0):
    """
    Рекурсивно решает задачу коммивояжера методом ветвей и границ.
    
    matrix -- матрица затрат (numpy.ndarray)
    current -- текущий город (int)
    visited -- множество посещённых городов (set)
    current_cost -- накопленная стоимость пути (float)
    path -- текущий путь (list)
    best -- словарь с лучшей найденной стоимостью и путём: {'cost': float, 'path': list}
    selected_edges -- выбранные ребра для предотвращения циклов (dict)
    verbose -- флаг для вывода промежуточных результатов (bool)
    depth -- глубина рекурсии (int, по умолчанию 0)
    """
    num_cities = len(matrix)

    # Если все города посещены, пытаемся вернуться в начальный город
    if len(visited) == num_cities:
        return_cost = matrix[current][0]
        if return_cost == float('inf'):
            return
        total_cost = current_cost + return_cost
        if total_cost < best['cost']:
            best['cost'] = total_cost
            best['path'] = path + [0]
        if verbose:
            print(f"Глубина={depth} ✅ Найден полный путь {path + [0]} с общей стоимостью {total_cost}")
        return

    # Формируем список кандидатов с сортировкой по стоимости перехода
    candidates = sorted(
        [city for city in range(num_cities) 
         if city not in visited and matrix[current][city] != inf],
        key=lambda city: matrix[current][city]
    )
    if verbose:
        print(f"Глубина={depth}  Рассматриваем кандидатов из города {current}: {candidates}")

    for next_city in candidates:
        cost_to_next = matrix[current][next_city]

        # Создаем новую матрицу и модифицируем её для текущего перехода
        new_matrix = matrix.copy()
        new_matrix[current, :] = inf
        new_matrix[:, next_city] = inf
        if len(visited) + 1 < num_cities:
            new_matrix[next_city][0] = inf
        if current in selected_edges:
            prev_city = selected_edges[current]
            new_matrix[next_city][prev_city] = inf

        # Копируем словарь выбранных ребер и обновляем его для текущего перехода
        new_selected_edges = selected_edges.copy()
        new_selected_edges[current] = next_city

        # Выполняем редукцию матрицы, возвращается новая матрица и стоимость редукции
        reduced_matrix, reduced_cost = reduce_cost_matrix(new_matrix, verbose)
        new_cost = current_cost + cost_to_next + reduced_cost

        # Оцениваем нижнюю границу, используя MST и сумму двух минимальных ребер
        remaining_cities = set(range(num_cities)) - visited - {next_city}
        mst_estimate = minimum_spanning_tree(reduced_matrix, remaining_cities, verbose) if remaining_cities else 0

        # Находим сумму двух минимальных ребер для оставшихся городов
        min_edges_sum = sum(sorted([min(row[row != inf]) for i, row in enumerate(reduced_matrix) if i in remaining_cities])[:2])

        lower_bound = new_cost + min(mst_estimate, min_edges_sum)

        if verbose:
            print(f"Глубина={depth} 🔍 Рассматриваем путь {path + [next_city]} (стоимость: {new_cost}, нижняя граница: {lower_bound})")

        # Продолжаем рекурсию только если нижняя граница ниже текущего лучшего результата
        if lower_bound < best['cost']:
            tsp_branch_and_bound(
                reduced_matrix, next_city, visited | {next_city}, new_cost,
                path + [next_city], best, new_selected_edges, verbose, depth + 1
            )


def tsp_little_algorithm(matrix, verbose=False):
    """
    Решает задачу коммивояжера с использованием алгоритма Литтла.
    
    matrix -- матрица затрат (numpy.ndarray)
    verbose -- флаг для вывода промежуточных результатов (bool)
    
    Возвращает:
    best_solution -- словарь с лучшим найденным путём и его стоимостью: {'cost': float, 'path': list}
    """
    if verbose:
        print("🚀 Запуск алгоритма Литтла...")
    best_solution = {'cost': float('inf'), 'path': []}
    reduced_matrix, initial_cost = reduce_cost_matrix(matrix, verbose)
    tsp_branch_and_bound(reduced_matrix, 0, {0}, initial_cost, [0], best_solution, {}, verbose)
    return best_solution


def tsp_nearest_neighbor(matrix, verbose=False):
    """Решает задачу коммивояжера с использованием алгоритма ближайшего соседа.
    
    Аргументы:
    matrix -- матрица затрат (numpy.ndarray)
    verbose -- флаг для вывода промежуточных результатов (bool, по умолчанию False)
    
    Возвращает:
    solution -- найденный путь и его стоимость (dict)
    """
    num_cities = len(matrix)
    visited = {0}
    path = [0]
    total_cost = 0
    current_city = 0
    while len(visited) < num_cities:
        next_city = min((i for i in range(num_cities) if i not in visited), key=lambda i: matrix[current_city][i], default=None)
        if next_city is None or matrix[current_city][next_city] == inf:
            return {'cost': inf, 'path': []}
        visited.add(next_city)
        path.append(next_city)
        total_cost += matrix[current_city][next_city]
        current_city = next_city
    if matrix[current_city][0] == inf:
        return {'cost': inf, 'path': []}
    path.append(0)
    total_cost += matrix[current_city][0]
    if verbose:
        print(f"🏁 Оптимальный путь найден: {path}, стоимость: {total_cost}")
    return {'cost': total_cost, 'path': path}

def solve_tsp(matrix, method='little', verbose=False):
    """Решает задачу коммивояжера выбранным методом.
    
    Аргументы:
    matrix -- матрица затрат (numpy.ndarray)
    method -- метод решения ('little' или 'nearest_neighbor') (str, по умолчанию 'little')
    verbose -- флаг для вывода промежуточных результатов (bool, по умолчанию False)
    
    Возвращает:
    solution -- найденный путь и его стоимость (dict)
    """
    return tsp_little_algorithm(matrix, verbose) if method == 'little' else tsp_nearest_neighbor(matrix, verbose)