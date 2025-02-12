import { performance } from 'perf_hooks';
import { Square, backtrack, initializeInitialSquares, findMaxSquareSize } from './alg-fast';
import chalk from 'chalk'; // Для цветного вывода в консоль
import Table from 'cli-table3'; // Для красивых таблиц

// Функция для замера времени выполнения алгоритма и использования памяти
function benchmarkAlgorithm(n: number, runs: number = 5): { avgTime: number; bestCount: number; operations: number; avgMemoryUsage: number } {
    let totalTime = 0;
    let totalOperations = 0;
    let totalMemoryUsage = 0;
    let bestCount = Infinity;

    for (let i = 0; i < runs; i++) {
        const operationCounter = { value: 0 };
        const squareSize = { value: 0 };
        const newGridSize = findMaxSquareSize(n, squareSize);
        const currentBestCount = { value: 2 * newGridSize + 1 };
        const squares = initializeInitialSquares(newGridSize);
        const bestSolution: Square[] = [];
        const initialOccupiedArea = squares[0].size ** 2 + 2 * squares[1].size ** 2;
        const startX = squares[2].bottom, startY = squares[2].x;    
        
        const startTime = performance.now();
        const startMemoryUsage = process.memoryUsage().heapUsed;
        backtrack(squares, initialOccupiedArea, 3, startX, startY, newGridSize, currentBestCount, bestSolution, operationCounter);
        const endMemoryUsage = process.memoryUsage().heapUsed;
        const endTime = performance.now();

        totalTime += endTime - startTime;
        totalOperations += operationCounter.value;
        totalMemoryUsage += endMemoryUsage - startMemoryUsage;
        if (currentBestCount.value < bestCount) {
            bestCount = currentBestCount.value;
        }
    }

    return {
        avgTime: totalTime / runs,
        bestCount: bestCount,
        operations: totalOperations / runs,
        avgMemoryUsage: totalMemoryUsage / runs,
    };
}

// Основная функция для тестирования
function runBenchmark() {
    const testCases = Array.from({ length: 57 }, (_, i) => i + 4);

    console.log(chalk.bold.blue('Benchmarking algorithm...\n'));

    // Создаем таблицу
    const table = new Table({
        head: [
            chalk.bold.green('n'),
            chalk.bold.green('Avg Time (ms)'),
            chalk.bold.green('Best Count'),
            chalk.bold.green('Avg Operations'),
            chalk.bold.green('Avg Memory Usage (bytes)')
        ],
        colWidths: [10, 20, 15, 20, 30],
        style: { head: ['cyan'], border: ['gray'] }
    });

    // Заполняем таблицу результатами
    for (const n of testCases) {
        const { avgTime, bestCount, operations, avgMemoryUsage } = benchmarkAlgorithm(n);
        table.push([
            chalk.yellow(n),
            chalk.cyan(avgTime.toFixed(4)),
            chalk.magenta(bestCount.toString()),
            chalk.white(operations.toFixed(0)),
            chalk.yellow(avgMemoryUsage.toFixed(0))
        ]);
    }

    // Выводим таблицу
    console.log(table.toString());
}

// Запуск тестирования
runBenchmark();