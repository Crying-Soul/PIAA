import * as readline from 'readline';
import { Square, backtrack, initializeInitialSquares, findMaxSquareSize } from './alghoritm';
import { visualizeGrid } from './visualization';

async function main() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    const operationCounter = { value: 0 };
    const gridSize: number = await new Promise((resolve) => {
        rl.question("Enter grid size: ", (answer: string) => {
            resolve(parseInt(answer, 10));
        });
    });

    const squareSize = { value: 0 };
    const newGridSize = findMaxSquareSize(gridSize, squareSize);
    const bestCount = { value: 2 * newGridSize + 1 };
    let squares = initializeInitialSquares(newGridSize);
    const bestSolution: Square[] = [];
    const initialOccupiedArea = squares[0].size ** 2 + 2 * squares[1].size ** 2;
    const startX = squares[2].bottom, startY = squares[2].x;   
    backtrack(squares, initialOccupiedArea, 3, startX, startY, newGridSize, bestCount, bestSolution, operationCounter);

    console.log(`Grid size: ${gridSize}`);
    console.log(`Operation count: ${operationCounter.value}`);
    console.log(`Best count: ${bestCount.value}`);
    for (const square of bestSolution) {
        console.log(`${1 + square.x * squareSize.value} ${1 + square.y * squareSize.value} ${square.size * squareSize.value}`);
    }
    visualizeGrid(newGridSize, bestSolution);
    rl.close();
}

main();