import { createCanvas } from 'canvas';
import { Square } from './alghoritm'; // Импортируйте тип Square, если он используется
import fs from 'fs';

/**
 * Функция для визуализации квадратов на холсте и сохранения изображения.
 * @param gridSize - Размер сетки.
 * @param squares - Массив квадратов для отрисовки.
 * @param outputPath - Путь для сохранения изображения.
 */
export function visualizeGrid(gridSize: number, squares: Square[], outputPath: string = './grid.png') {
    const canvasSize = 500; // Размер холста
    const canvas = createCanvas(canvasSize, canvasSize);
    const ctx = canvas.getContext('2d');

    const cellSize = canvasSize / gridSize;

    // Отрисовка сетки
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    for (let i = 0; i <= gridSize; i++) {
        ctx.beginPath();
        ctx.moveTo(i * cellSize, 0);
        ctx.lineTo(i * cellSize, canvasSize);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, i * cellSize);
        ctx.lineTo(canvasSize, i * cellSize);
        ctx.stroke();
    }

    // Отрисовка квадратов
    const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']; // Цвета для квадратов
    squares.forEach((square, index) => {
        ctx.fillStyle = colors[index % colors.length];
        ctx.fillRect(
            square.x * cellSize,
            square.y * cellSize,
            square.size * cellSize,
            square.size * cellSize
        );
    });

    // Сохранение изображения
    const out = fs.createWriteStream(outputPath);
    const stream = canvas.createPNGStream();
    stream.pipe(out);
    out.on('finish', () => console.log(`Изображение сохранено в ${outputPath}`));
}