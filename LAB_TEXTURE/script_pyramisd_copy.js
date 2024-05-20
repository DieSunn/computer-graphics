class Pyramid {
  constructor(baseVertices, height, x, y,textureImage ) {
    this.baseVertices = baseVertices;
    this.height = height;
    this.x = x;
    this.y = y;
    this.vertices = this.calculateVertices();
    this.faces = this.calculateFaces();
    this.calculateNormals();
    this.textureCoordinates = this.calculateTextureCoordinates();
    this.textureImage = textureImage; // Изображение текстуры

  }

  calculateVertices() {
    const vertices = [];
    const baseVertexCount = this.baseVertices.length;
    const topVertex = new Point(this.y, this.x, 300);

    vertices.push(topVertex);
    for (let i = 0; i < baseVertexCount; i++) {
      vertices.push(this.baseVertices[i]);
    }
    return vertices;
  }
  // Метод для сдвига текстурных координат
  textureShift(du, dv) {
    for (let texCoord of this.textureCoordinates) {
      texCoord.u += du;
      texCoord.v += dv;
    }
  }
  // Метод для расчета текстурных координат вершин
  calculateTextureCoordinates() {
    // Здесь вы можете рассчитать текстурные координаты для каждой вершины пирамиды
    // Вершины на базе могут иметь текстурные координаты от (0, 0) до (1, 1),
    // а вершина на вершине (0.5, 0.5) для центрирования текстуры.
    // Это просто пример, ваш метод может быть более сложным в зависимости от требований.
    const textureCoordinates = [];
    const baseVertexCount = this.baseVertices.length;
    for (let i = 0; i < baseVertexCount; i++) {
      textureCoordinates.push({ u: i / baseVertexCount, v: 0 });
    }
    textureCoordinates.push({ u: 0.5, v: 0.5 }); // Текстурные координаты для вершины на вершине
    return textureCoordinates;
  }
  calculateFaces() {
    const baseVertexCount = this.baseVertices.length;
    const faces = [];

    for (let i = 0; i < baseVertexCount; i++) {
      const face = [
        this.vertices[0],
        this.vertices[i + 1],
        this.vertices[(i + 1) % baseVertexCount + 1]
      ];
      faces.push(face);
    }

    const bottomFace = this.baseVertices.slice();
    bottomFace.reverse();
    faces.push(bottomFace);

    return faces;
  }
  /// Расчет нормалей к граням
  calculateNormals() {
    this.normals = []; // Создание пустого массива для хранения нормалей.

    for (let face of this.faces) { // Проход по всем граням модели.
      // Вычисление векторов v1 и v2 для текущей грани.
      const v1 = new Point(
        face[1].x - face[0].x,
        face[1].y - face[0].y,
        face[1].z - face[0].z
      );
      const v2 = new Point(
        face[2].x - face[0].x,
        face[2].y - face[0].y,
        face[2].z - face[0].z
      );

      // Вычисление нормали к текущей грани.
      const normal = new Point(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
      );

      // Нормализация нормали.
      const magnitude = Math.sqrt(
        normal.x * normal.x + normal.y * normal.y + normal.z * normal.z
      );
      normal.x /= magnitude;
      normal.y /= magnitude;
      normal.z /= magnitude;

      // Добавление нормали в массив normals.
      this.normals.push(normal);
    }
  }

  rotate(deg, t0) {
    for (let vertex of this.vertices) { // Проход по всем вершинам модели.
      vertex.rotate(deg, t0); // Поворот текущей вершины.
    }
  }

  projection(type, tv, d) {
    const projectionArr = []; // Создание пустого массива для хранения проекций.

    for (let face of this.faces) { // Проход по всем граням модели.
      const p = []; // Создание временного массива для хранения проекций текущей грани.
      p.dist = 0; // Инициализация переменной для хранения суммарного расстояния проекций.

      for (let vertex of face) { // Проход по вершинам текущей грани.
        const proj = vertex.projection(type, tv, d); // Получение проекции текущей вершины.
        p.dist += proj.dist; // Добавление расстояния проекции к общему расстоянию.
        p.push(proj); // Добавление проекции в массив проекций грани.
      }

      // Определение направления обхода грани и добавление в массив.
      p.clock = ((p[1].x - p[0].x) * (p[2].y - p[0].y) - (p[1].y - p[0].y) * (p[2].x - p[0].x)) < 0;
      projectionArr.push(p); // Добавление массива проекций текущей грани в массив всех проекций.
    }

    return projectionArr; // Возвращение массива всех проекций.
  }

};

class Point {
  // координаты точки
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
  // поворачиваем эту точку на угол (deg)
  // по осям (x,y,z) относительно точки (t0)
  rotate(deg, t0) {
    // функции для получения синуса и косинуса угла в радианах
    const sin = (deg) => Math.sin((Math.PI / 180) * deg);
    const cos = (deg) => Math.cos((Math.PI / 180) * deg);
    // матрицы поворота для трёхмерного пространства
    let x, y, z;
    // поворот по оси 'x'
    y = t0.y + (this.y - t0.y) * cos(deg.x) - (this.z - t0.z) * sin(deg.x);
    z = t0.z + (this.y - t0.y) * sin(deg.x) + (this.z - t0.z) * cos(deg.x);
    this.y = y; this.z = z;
    // поворот по оси 'y'
    x = t0.x + (this.x - t0.x) * cos(deg.y) - (this.z - t0.z) * sin(deg.y);
    z = t0.z + (this.x - t0.x) * sin(deg.y) + (this.z - t0.z) * cos(deg.y);
    this.x = x; this.z = z;
    // поворот по оси 'z'
    x = t0.x + (this.x - t0.x) * cos(deg.z) - (this.y - t0.y) * sin(deg.z);
    y = t0.y + (this.x - t0.x) * sin(deg.z) + (this.y - t0.y) * cos(deg.z);
    this.x = x; this.y = y;
  }


  // получаем проекцию типа (type) с расстояния (d)
  // на плоскость экрана наблюдателя (tv)
  projection(tv, d) {
    let proj = {};
    // получаем проекцию по экспериментальным формулам
    proj.x = this.x;
    proj.y = this.y;

    // вычисляем расстояние до центра проекции
    proj.dist = Math.sqrt((this.x - tv.x) * (this.x - tv.x)
      + (this.y - tv.y) * (this.y - tv.y)
      + (this.z - tv.z + d) * (this.z - tv.z + d));
    return proj;
  }

};

'use strict';
const canvas1 = document.getElementById('canvas1'); // Получение ссылки на элемент canvas по его id.
const canvasWidth = canvas1.width; // Получение ширины canvas.
const canvasHeight = canvas1.height; // Получение высоты canvas.
let pyramid = null; // Инициализация переменной для хранения пирамиды.
let t0 = null; // Инициализация переменной для хранения точки t0.

/// Функция для создания пирамиды.
function createPyramid(texture1) {
  const baseVertexCountInput = document.getElementById('cubeSizeInput'); // Получение ссылки на элемент ввода.
  const baseVertexCount = parseInt(baseVertexCountInput.value); // Получение количества вершин основания.
  const height = 100; // Задание высоты пирамиды.

  const baseVertices = calculateBaseVertices(baseVertexCount); // Вычисление вершин основания.

  const pyramidCenterX = canvasWidth / 2; // Вычисление центра пирамиды по оси X.
  const pyramidCenterY = canvasHeight / 2; // Вычисление центра пирамиды по оси Y.
  const pyramidCenterZ = height / 2; // Вычисление центра пирамиды по оси Z.

  const texture = new Image();
  texture.onload = () => { // Обработчик события загрузки изображения
    pyramid = new Pyramid(baseVertices, height, pyramidCenterY, pyramidCenterX, texture); // Создание пирамиды
    t0 = new Point(pyramidCenterX, pyramidCenterY, pyramidCenterZ); // Инициализация точки t0
    repaint(); // Перерисовка
  };
  texture.src = texture1;
}


// Функция для вычисления вершин основания пирамиды.
function calculateBaseVertices(vertexCount) {
  const baseRadius = 200; // Радиус основания пирамиды.
  const baseCenterX = canvasWidth / 2; // X-координата центра основания пирамиды.
  const baseCenterY = canvasHeight / 2; // Y-координата центра основания пирамиды.

  const baseVertices = []; // Массив для хранения вершин основания.
  const angleIncrement = (2 * Math.PI) / vertexCount; // Вычисление угла между вершинами.
  let angle = 0; // Инициализация начального угла.

  // Цикл для вычисления координат вершин основания.
  for (let i = 0; i < vertexCount; i++) {
    const x = baseCenterX + baseRadius * Math.cos(angle); // Вычисление X-координаты вершины.
    const y = baseCenterY + baseRadius * Math.sin(angle); // Вычисление Y-координаты вершины.
    const z = 0; // Задание Z-координаты вершины.
    baseVertices.push(new Point(x, y, z)); // Добавление вершины в массив.
    angle += angleIncrement; // Увеличение угла для следующей вершины.
  }

  return baseVertices; // Возвращение массива вершин основания.
}

const tv = new Point(150, 150, 150); // Инициализация точки обзора.
const deg = { x: 0, y: 0, z: 0 }; // Инициализация углов поворота.

function repaint() {
  if (pyramid) {
    pyramid.rotate(deg, t0); // Поворот пирамиды.
    pyramid.calculateNormals(); // Расчет нормалей к граням.
    drawFigureWithTexture(canvas1, pyramid.textureImage); // Передача текстурного изображения
  }
}


let colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']; // Массив цветов для граней пирамиды.

// Функция для отрисовки пирамиды с использованием текстуры
function drawFigureWithTexture(canvas, textureImage) {
  const context = canvas.getContext('2d');
  context.clearRect(0, 0, canvas.width, canvas.height);

  const texturePattern = context.createPattern(textureImage, 'repeat'); // Создание паттерна текстуры
  if (texturePattern) {
    context.fillStyle = texturePattern;
    context.strokeStyle = 'white'; // Установка цвета обводки

    for (const face of pyramid.faces) { // Используем pyramid.faces напрямую, так как метод не находится внутри класса Pyramid
      context.beginPath();
      for (let j = 0; j < face.length; j++) {
        const vertex = face[j];
        const x = vertex.x;
        const y = vertex.y;

        if (j === 0) {
          context.moveTo(x, y);
        } else {
          context.lineTo(x, y);
        }
      }
      context.closePath();
      context.fill();
      context.stroke(); // Отрисовка обводки
    }

    // Отрисовка ребер пирамиды
    context.strokeStyle = 'black'; // Цвет обводки ребер
    context.lineWidth = 1; // Толщина линий

    for (const face of pyramid.faces) {
      context.beginPath();
      for (let j = 0; j < face.length; j++) {
        const vertex = face[j];
        const x = vertex.x;
        const y = vertex.y;

        if (j === 0) {
          context.moveTo(x, y);
        } else {
          context.lineTo(x, y);
        }
      }
      context.closePath();
      context.stroke();
    }
  }
}




// Обработчик изменения состояния чекбоксов.
function handleCheckboxChange() {
  const checkboxForm = document.getElementById('checkboxForm'); // Получение ссылки на форму чекбоксов.
  const checkboxX = checkboxForm.elements['checkboxX']; // Получение ссылки на чекбокс по имени.
  const checkboxY = checkboxForm.elements['checkboxY']; // Получение ссылки на чекбокс по имени.
  const checkboxZ = checkboxForm.elements['checkboxZ']; // Получение ссылки на чекбокс по имени.

  // Установка углов поворота в зависимости от состояния чекбоксов.
  deg.x = checkboxX.checked ? 2 : 0;
  deg.y = checkboxY.checked ? 2 : 0;
  deg.z = checkboxZ.checked ? 2 : 0;
}

// Задание частоты обновления изображения (20 Гц) после загрузки документа.
document.addEventListener('DOMContentLoaded', () => {
  setInterval(repaint, 50); // Вызов функции перерисовки с интервалом.
  
  const checkboxForm = document.getElementById('checkboxForm'); // Получение ссылки на форму чекбоксов.
  checkboxForm.addEventListener('change', handleCheckboxChange); // Установка обработчика на изменение чекбоксов.
});