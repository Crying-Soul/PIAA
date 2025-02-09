import { performance } from 'perf_hooks';
import { Square, backtrack, initializeInitialSquares, findMaxSquareSize } from './alghoritm'; 

// Функция для замера времени выполнения алгоритма
function benchmarkAlgorithm(n: number): { time: number; bestCount: number } {
    const operationCounter = { value: 0 };
    const squareSize = { value: 0 };
    const newGridSize = findMaxSquareSize(n, squareSize); // Используем новую функцию
    const bestCount = { value: 2 * newGridSize + 1 };
    const squares = initializeInitialSquares(newGridSize); // Используем новую функцию
    const bestSolution: Square[] = [];
    const initialOccupiedArea = Math.pow(Math.floor((newGridSize + 1) / 2), 2) + 2 * Math.pow(Math.floor(newGridSize / 2), 2);
    const startX = Math.floor(newGridSize / 2), startY = Math.floor((newGridSize + 1) / 2);

    const startTime = performance.now(); // Засекаем начальное время
    backtrack(squares, initialOccupiedArea, 3, startX, startY, newGridSize, bestCount, bestSolution, operationCounter); // Используем обновленные параметры
    const endTime = performance.now(); // Засекаем конечное время

    return {
        time: endTime - startTime, // Время выполнения в миллисекундах
        bestCount: bestCount.value, // Лучшее количество квадратов
    };
}

// Основная функция для тестирования
function runBenchmark() {
    const testCases = [4, 5, 6, 7, 8, 9, 10, 15, 19, 20]; // Тестовые значения n

    console.log('Benchmarking algorithm...');
    console.log('n\tTime (ms)\tBest Count');
    console.log('----------------------------------');

    for (const n of testCases) {
        const { time, bestCount } = benchmarkAlgorithm(n); // Замеряем время и получаем результат
        console.log(`${n}\t${time.toFixed(2)}\t\t${bestCount}`); // Выводим результаты
    }
}

// Запуск тестирования
runBenchmark();