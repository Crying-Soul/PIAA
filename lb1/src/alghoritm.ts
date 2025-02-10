export class Square {
    public readonly right: number;
    public readonly bottom: number;

    constructor(
        public readonly x: number,
        public readonly y: number,
        public readonly size: number
    ) {
        this.right = x + size;
        this.bottom = y + size;
    }
}

export function isOverlapping(squares: Square[], x: number, y: number): boolean {
    for (const square of squares) {
        if (x >= square.x && x < square.right && y >= square.y && y < square.bottom) {
            return true;
        }
    }
    return false;
}

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

    if (occupiedArea === gridSize * gridSize) {
        if (currentCount < bestCount.value) {
            bestCount.value = currentCount;
            bestSolution.length = 0;
            bestSolution.push(...squares);
        }
        return;
    }

    for (let x = startX; x < gridSize; x++) {
        for (let y = startY; y < gridSize; y++) {
            if (isOverlapping(squares, x, y)) continue;

            let maxSize = Math.min(gridSize - x, gridSize - y);

            for (const square of squares) {
                if (square.right > x && square.y > y) {
                    maxSize = Math.min(maxSize, square.y - y);
                } else if (square.bottom > y && square.x > x) {
                    maxSize = Math.min(maxSize, square.x - x);
                }
            }

            if (maxSize <= 0) continue;

            for (let size = maxSize; size >= 1; size--) {
                const newSquare = new Square(x, y, size);
                const newOccupiedArea = occupiedArea + size * size;

                const remainingArea = gridSize * gridSize - newOccupiedArea;
                if (remainingArea > 0) {
                    const maxPossibleSize = Math.min(gridSize - x, gridSize - y);
                    const minSquaresNeeded = Math.ceil(remainingArea / (maxPossibleSize * maxPossibleSize));
                    if (currentCount + 1 + minSquaresNeeded >= bestCount.value) {
                        continue;
                    }
                }

                squares.push(newSquare);
                if (newOccupiedArea === gridSize * gridSize) {
                    if (currentCount + 1 < bestCount.value) {
                        bestCount.value = currentCount + 1;
                        bestSolution.length = 0;
                        bestSolution.push(...squares);
                    }
                    squares.pop();
                    continue;
                }

                if (currentCount + 1 < bestCount.value) {
                    backtrack(
                        squares,
                        newOccupiedArea,
                        currentCount + 1,
                        x,
                        y,
                        gridSize,
                        bestCount,
                        bestSolution,
                        operationCounter
                    );
                }
                squares.pop();
            }
            return;
        }
        startY = 0;
    }
}

export function initializeInitialSquares(gridSize: number): Square[] {
    const halfSize = Math.floor((gridSize + 1) / 2);
    const smallSize = Math.floor(gridSize / 2);
    return [
        new Square(0, 0, halfSize),
        new Square(0, halfSize, smallSize),
        new Square(halfSize, 0, smallSize)
    ];
}

export function findMaxSquareSize(gridSize: number, squareSize: { value: number }): number {
    let maxDivisor = 1;
    for (let i = Math.floor(gridSize / 2); i >= 1; i--) {
        if (gridSize % i === 0) {
            maxDivisor = i;
            break;
        }
    }
    squareSize.value = maxDivisor;
    return gridSize / maxDivisor;
}