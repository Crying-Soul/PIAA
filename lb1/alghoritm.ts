export class Square {
    constructor(
        public readonly x: number,
        public readonly y: number,
        public readonly size: number
    ) { }
}

export function isOverlapping(squares: Square[], x: number, y: number): boolean {
    return squares.some(({ x: sx, y: sy, size }) =>
        x >= sx && x < sx + size && y >= sy && y < sy + size
    );
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
            for (const { x: sx, y: sy, size } of squares) {
                if (sx + size > x && sy > y) maxSize = Math.min(maxSize, sy - y);
            }

            for (let size = maxSize; size >= 1; size--) {
                const newSquare = new Square(x, y, size);
                const newOccupiedArea = occupiedArea + size * size;

                if (newOccupiedArea === gridSize * gridSize) {
                    if (currentCount + 1 < bestCount.value) {
                        bestCount.value = currentCount + 1;
                        bestSolution.length = 0;
                        bestSolution.push(...squares, newSquare);
                    }
                    return;
                }

                if (currentCount + 1 < bestCount.value) {
                    backtrack(
                        [...squares, newSquare],
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
    let maxDivisor = 2;
    for (let i = 1; i <= gridSize / 2; i++) {
        if (gridSize % i === 0) maxDivisor = i;
    }
    squareSize.value = maxDivisor;
    return gridSize / maxDivisor;
}
