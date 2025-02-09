export class Square {
    x: number;
    y: number;
    size: number;

    constructor(x: number, y: number, size: number) {
        this.x = x;
        this.y = y;
        this.size = size;
    }
}

// Проверяет, перекрывает ли заданный квадрат другие квадраты в данной карте
export function isOverlapping(squares: Square[], x: number, y: number): boolean {
    for (const square of squares) {
        if (x >= square.x && x < square.x + square.size && y >= square.y && y < square.y + square.size) {
            return true;
        }
    }
    return false;
}

// Рекурсивная функция, реализующая алгоритм обхода дерева решений
export function backtrack(
    squares: Square[],
    occupiedArea: number,
    currentCount: number,
    startX: number,
    startY: number,
    gridSize: number,
    bestCount: { value: number },
    bestSolution: Square[],
    operationCounter: { value: number }
) {
    operationCounter.value++;
    for (let x = startX; x < gridSize; ++x) {
        for (let y = startY; y < gridSize; ++y) {
            if (!isOverlapping(squares, x, y)) {
                let maxSize = Math.min(gridSize - 1, Math.min(gridSize - x, gridSize - y));
                for (const square of squares) {
                    if (square.x + square.size > x && square.y > y) {
                        maxSize = Math.min(maxSize, square.y - y);
                    }
                }

                for (let size = maxSize; size >= 1; --size) {
                    const newSquare = new Square(x, y, size);
                    const newSolution = [...squares, newSquare];

                    if (occupiedArea + Math.pow(newSquare.size, 2) === gridSize * gridSize) {
                        if (currentCount + 1 < bestCount.value) {
                            bestCount.value = currentCount + 1;
                            bestSolution.length = 0;
                            bestSolution.push(...newSolution);
                        }
                    } else {
                        if (currentCount + 1 < bestCount.value) {
                            backtrack(newSolution, occupiedArea + Math.pow(newSquare.size, 2), currentCount + 1, startX, startY, gridSize, bestCount, bestSolution, operationCounter);
                        } else {
                            return;
                        }
                    }
                }
                return;
            }
        }
        startX = Math.floor(gridSize / 2);
        startY = 0;
    }
}

// Инициализация начальной карты, состоящей из трех квадратов
export function initializeInitialSquares(gridSize: number): Square[] {
    const squares: Square[] = [];
    squares.push(new Square(0, 0, Math.floor((gridSize + 1) / 2)));
    squares.push(new Square(0, Math.floor((gridSize + 1) / 2), Math.floor(gridSize / 2)));
    squares.push(new Square(Math.floor((gridSize + 1) / 2), 0, Math.floor(gridSize / 2)));
    return squares;
}

// Функция для определения максимального размера квадрата, на которые можно разбить столешницу
export function findMaxSquareSize(gridSize: number, squareSize: { value: number }): number {
    squareSize.value = 2;
    for (let i = 1; i <= gridSize / 2; ++i) {
        if (gridSize % i === 0) {
            squareSize.value = i;
        }
    }
    return gridSize / squareSize.value;
}

