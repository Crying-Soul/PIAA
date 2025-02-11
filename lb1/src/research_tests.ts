import { Square, backtrack, initializeInitialSquares, findMaxSquareSize } from './alg-fast';
import { createChart } from './charts';

async function researchOperations() {
    const operationCounter = { value: 0 };
    const gridSizes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59];
    const results: { n: number, operations: number }[] = []; // Массив для хранения результатов

    for (const gridSize of gridSizes) {
        const squareSize = { value: 0 };
        const newGridSize = findMaxSquareSize(gridSize, squareSize);
        const bestCount = { value: 2 * newGridSize + 1 };
        let squares = initializeInitialSquares(newGridSize);
        const bestSolution: Square[] = [];
        const initialOccupiedArea = squares[0].size ** 2 + 2 * squares[1].size ** 2;
        const startX = squares[2].bottom, startY = squares[2].x;    

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