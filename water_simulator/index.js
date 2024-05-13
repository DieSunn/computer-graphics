// Подключаем необходимые библиотеки
const gl = require('gl')(800, 600, { preserveDrawingBuffer: true });
const THREE = require('three');

// Создаем сцену
var scene = new THREE.Scene();

// Создаем камеру
var camera = new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000);
camera.position.z = 5;

// Создаем рендерер
var renderer = new THREE.WebGLRenderer({ context: gl });
renderer.setSize(800, 600);

// Создаем геометрию вокселя
var geometry = new THREE.BoxGeometry(1, 1, 1);

// Создаем материал воды
var material = new THREE.MeshBasicMaterial({color: 0x0000ff, transparent: true, opacity: 0.6});

// Создаем воксель воды
var cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Функция анимации
function animate() {
    // Вращаем воксель воды
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);

    // Запускаем следующий кадр анимации
    setImmediate(animate);
}

// Запускаем анимацию
animate();
