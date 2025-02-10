import { Square, backtrack, initializeInitialSquares, findMaxSquareSize } from './alg-fast';
import { createChart } from './charts';

async function researchOperations() {
    const operationCounter = { value: 0 };
    const gridSizes = Array.from({ length: 57 }, (_, i) => i + 4);
    const results: { n: number, operations: number }[] = []; // Массив для хранения результатов

    for (const gridSize of gridSizes) {
        const squareSize = { value: 0 };
        const newGridSize = findMaxSquareSize(gridSize, squareSize);
        const bestCount = { value: 2 * newGridSize + 1 };
        let squares = initializeInitialSquares(newGridSize);
        const bestSolution: Square[] = [];
        const initialOccupiedArea = Math.pow(Math.floor((newGridSize + 1) / 2), 2) + 2 * Math.pow(Math.floor(newGridSize / 2), 2);
        const startX = Math.floor(newGridSize / 2), startY = Math.floor((newGridSize + 1) / 2);

        operationCounter.value = 0; // Сброс счетчика операций для каждого размера сетки

        backtrack(squares, initialOccupiedArea, 3, startX, startY, newGridSize, bestCount, bestSolution, operationCounter);

        console.log(`Grid size: ${gridSize}`);
        console.log(`Operation count: ${operationCounter.value}`);
        console.log(`Best count: ${bestCount.value}`);
        for (const square of bestSolution) {
            console.log(`${1 + square.x * squareSize.value} ${1 + square.y * squareSize.value} ${square.size * squareSize.value}`);
        }
        console.log('-----------------------------');

        // Сохраняем результаты для построения графика
        results.push({ n: gridSize, operations: operationCounter.value });
    }

    // Строим график на основе результатов
    createChart(results);
}

researchOperations();