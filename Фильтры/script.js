// Класс ConvolutionFilter для применения свертки к изображению с помощью заданного ядра

class ConvolutionFilter {
    constructor(kernel) {
        this.kernel = kernel; // Сохраняем переданное ядро свертки
        this.kernelSize = Math.sqrt(kernel.length); // Определяем размер ядра, вычисляя квадратный корень из длины массива
        this.halfKernelSize = Math.floor(this.kernelSize / 2); // Определяем половину размера ядра, округляя результат деления размера ядра на 2 вниз
    }

    apply(imageData) {
        const width = imageData.width; // Ширина изображения
        const height = imageData.height; // Высота изображения
        const data = imageData.data; // Пиксельные данные изображения
        const outputData = new Uint8ClampedArray(data.length); // Создаем новый массив для хранения выходных данных

        // Проходим по каждому пикселю изображения
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                let sumR = 0, sumG = 0, sumB = 0; // Инициализируем суммы каналов R, G, B

                // Проходим по каждому элементу ядра свертки
                for (let ky = 0; ky < this.kernelSize; ky++) {
                    for (let kx = 0; kx < this.kernelSize; kx++) {
                        const imgX = x + kx - this.halfKernelSize; // Вычисляем координату X для пикселя изображения
                        const imgY = y + ky - this.halfKernelSize; // Вычисляем координату Y для пикселя изображения

                        // Проверяем, находится ли пиксель внутри границ изображения
                        if (imgX >= 0 && imgX < width && imgY >= 0 && imgY < height) {
                            const offset = (imgY * width + imgX) * 4; // Вычисляем смещение для получения данных о пикселе изображения
                            const weight = this.kernel[ky * this.kernelSize + kx]; // Получаем вес из ядра свертки
                            sumR += data[offset] * weight; // Суммируем значения канала R с учетом веса
                            sumG += data[offset + 1] * weight; // Суммируем значения канала G с учетом веса
                            sumB += data[offset + 2] * weight; // Суммируем значения канала B с учетом веса
                        }
                    }
                }

                const offset = (y * width + x) * 4; // Вычисляем смещение для получения данных о текущем пикселе
                outputData[offset] = sumR; // Устанавливаем значение канала R в выходных данных
                outputData[offset + 1] = sumG; // Устанавливаем значение канала G в выходных данных
                outputData[offset + 2] = sumB; // Устанавливаем значение канала B в выходных данных
                outputData[offset + 3] = data[offset + 3]; // Устанавливаем значение канала Alpha (прозрачности) в выходных данных
            }
        }

        return new ImageData(outputData, width, height); // Возвращаем новый объект ImageData с выходными данными
    }
}


// Создаем класс для обработки изображений
class ImageProcessor {
    constructor() {
        this.filters = {
            blur: [
                1 / 9, 1 / 9, 1 / 9,
                1 / 9, 1 / 9, 1 / 9,
                1 / 9, 1 / 9, 1 / 9
            ],
            edgeDetection: [
                -1, -1, -1,
                -1, 8, -1,
                -1, -1, -1
            ],
            sharpen: [
                0, -1, 0,
                -1, 5, -1,
                0, -1, 0
            ]
            // Добавьте другие фильтры по желанию
        };
    }

    applyFilter(filterName, imageData) {
        const filter = new ConvolutionFilter(this.filters[filterName]);
        return filter.apply(imageData);
    }
    applyCustomFilter(coefficients, imageData) {
        // Преобразуем каждое значение в число
        const parsedCoefficients = coefficients.map(Number);

        // Проверяем, нужна ли нормализация коэффициентов
        const sum = parsedCoefficients.reduce((acc, curr) => acc + curr, 0);
        const needNormalization = Math.abs(sum - 1) > Number.EPSILON;

        // Нормализуем коэффициенты, если это необходимо
        const normalizedCoefficients = needNormalization ? parsedCoefficients.map(coef => coef / sum) : parsedCoefficients;

        // Применяем фильтр с нормализованными или исходными коэффициентами
        const filter = new ConvolutionFilter(normalizedCoefficients);
        return filter.apply(imageData);
    }

}