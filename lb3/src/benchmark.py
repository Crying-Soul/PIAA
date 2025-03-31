import time
import random
import string
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Tuple, List
from levenshtein_calculator import LevenshteinCalculator
from multiprocessing import Pool, cpu_count
from functools import partial

def generate_test_strings(length: int, complexity: float) -> Tuple[str, str]:
    """Генерирует тестовые строки с заданной длиной и сложностью различий."""
    if length == 0:
        return "", ""
    
    base = ''.join(random.choices(string.ascii_letters, k=length))
    
    if complexity == 0:
        return base, base
    
    if complexity == 1:
        return base, ''.join(random.choices(string.ascii_letters, k=length))
    
    changes = max(1, int(length * complexity))
    indices = random.sample(range(length), changes)
    target = list(base)
    for i in indices:
        target[i] = random.choice(string.ascii_letters.replace(target[i], ''))
    return base, ''.join(target)

def run_single_test(args: Tuple[int, float]) -> Tuple[int, float]:
    """Выполняет один тест для multiprocessing."""
    length, complexity = args
    lev = LevenshteinCalculator()
    s1, s2 = generate_test_strings(length, complexity)
    
    start = time.perf_counter()
    distance = lev.calculate(s1, s2, False)
    elapsed = (time.perf_counter() - start) * 1000
    
    return distance, elapsed

def run_complexity_tests(repeats: int = 3) -> Dict[int, Dict[float, Tuple[float, float]]]:
    """Тесты с разной сложностью строк."""
    print("Running complexity tests...")
    
    lengths = [10, 50, 100, 500, 1000, 2000]
    complexities = [0, 0.25, 0.5, 0.75, 1.0]
    results = {length: {} for length in lengths}
    
    with Pool(processes=cpu_count()) as pool:
        for length in lengths:
            for complexity in complexities:
                # Создаем список аргументов для каждого повторения
                args = [(length, complexity) for _ in range(repeats)]
                test_results = pool.map(run_single_test, args)
                
                distances, times = zip(*test_results)
                avg_distance = np.mean(distances)
                avg_time = np.mean(times)
                results[length][complexity] = (avg_distance, avg_time)
                
                print(f"Length: {length}, Complexity: {complexity:.2f}, "
                      f"Avg Distance: {avg_distance:.1f}, Avg Time: {avg_time:.4f}ms")
    
    return results

def plot_complexity_results(results: Dict[int, Dict[float, Tuple[float, float]]]):
    """Визуализация результатов тестов сложности."""
    plt.figure(figsize=(15, 10))
    colors = plt.cm.viridis(np.linspace(0, 1, len(results)))
    
    # График времени выполнения
    plt.subplot(2, 1, 1)
    for length, color in zip(sorted(results.keys()), colors):
        complexities = sorted(results[length].keys())
        times = [results[length][c][1] for c in complexities]
        plt.plot(complexities, times, label=f'Length {length}', 
                 marker='o', color=color, linestyle='-')
    
    plt.title('Execution Time by String Complexity')
    plt.xlabel('Complexity')
    plt.ylabel('Time (ms, log scale)')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    
    # График расстояния Левенштейна
    plt.subplot(2, 1, 2)
    for length, color in zip(sorted(results.keys()), colors):
        complexities = sorted(results[length].keys())
        distances = [results[length][c][0] for c in complexities]
        plt.plot(complexities, distances, label=f'Length {length}', 
                 marker='o', color=color, linestyle='-')
    
    plt.title('Levenshtein Distance by String Complexity')
    plt.xlabel('Complexity')
    plt.ylabel('Distance')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('levenshtein_complexity.png', dpi=300)
    plt.show()

def run_length_tests(max_length: int = 5000, step: int = 250, repeats: int = 3):
    """Тест производительности при увеличении длины строк."""
    print("\nRunning length tests...")
    
    lengths = list(range(step, max_length + 1, step))
    if not lengths:
        lengths = [step]
    
    results = []
    
    with Pool(processes=cpu_count()) as pool:
        for length in lengths:
            args = [(length, 0.5) for _ in range(repeats)]  # средняя сложность
            test_results = pool.map(run_single_test, args)
            _, times = zip(*test_results)
            avg_time = np.mean(times)
            results.append((length, avg_time))
            
            print(f"Length: {length}, Avg Time: {avg_time:.4f}ms")
    
    # График зависимости времени от длины строк
    lengths, times = zip(*results)
    
    plt.figure(figsize=(12, 7))
    plt.plot(lengths, times, marker='o', linestyle='-', color='b')
    
    plt.title('Levenshtein Algorithm Performance by String Length')
    plt.xlabel('String Length')
    plt.ylabel('Time (ms, log scale)')
    plt.yscale('log')
    plt.grid(True)
    
    # Теоретическая сложность O(n²) для сравнения
    x = np.array(lengths)
    y = x**2 * (times[-1] / (lengths[-1]**2))
    plt.plot(x, y, 'r--', label='O(n²) reference')
    plt.legend()
    
    plt.savefig('levenshtein_performance.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    # Тесты с разной сложностью
    complexity_results = run_complexity_tests(repeats=5)
    plot_complexity_results(complexity_results)
    
    # Тест на увеличение длины строк
    run_length_tests(max_length=5000, step=500)