import tkinter as tk  # Библиотека для создания графического интерфейса
import cv2  # Библиотека для работы с изображениями
import matplotlib.pyplot as plt  # Библиотека для создания графиков
import numpy as np  # Библиотека для работы с массивами

def open_image():  # Функция для открытия изображения и создания гистограммы
    file_path = filedialog.askopenfilename(
        title="Открыть изображение",  # Заголовок диалогового окна
        filetypes=(  # Список допустимых типов файлов
            ("Изображения", "*.jpg, *.jpeg, *.png, *.bmp"),
            ("Все файлы", "*.*")
        )
    )
    img_label.config(text=file_path)  # Изменение текста метки
    img_label.update()  # Обновление метки
    create_histogram(file_path)  # Создание гистограммы

def create_histogram(file_path):  # Функция для создания гистограммы изображения
    img = cv2.imread(file_path)  # Загрузка изображения
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Преобразование изображения в цветовую модель HSV
    h, s, v = cv2.split(hsv)  # Разделение изображения на компоненты H, S, V
    bins = np.int32(np.linspace(0, 255, 256))[:, np.newaxis]  # Создание массива для хранения гистограммы
    hist_h = np.bincount(np.int32(h), bins, minlength=256)  # Создание гистограммы для компонента H
    hist_s = np.bincount(np.int32(s), bins, minlength=256)  # Создание гистограммы для компонента S
    hist_v = np.bincount(np.int32(v), bins, minlength=256)  # Создание гистограммы для компонента V
    hist_h = hist_h / np.sum(hist_h)  # Нормализация гистограммы для компонента H
    hist_s = hist_s / np.sum(hist_s)  # Нормализация гистограммы для компонента S
    hist_v = hist_v / np.sum(hist_v)  # Нормализация гистограммы для компонента V
    plt.figure()  # Создание нового графика
    plt.subplot(311)  # Создание первого подграфика
    plt.plot(hist_h, color='b')  # Отображение гистограммы для компонента H
    plt.xlim([0, 256])  # Установка диапазона отображения по оси X
    plt.subplot(312)  # Создание второго подграфика
    plt.plot(hist_s, color='g')  # Отображение гистограммы для компонента S
    plt.xlim([0, 256])  # Установка диапазона отображения по оси X
    plt.subplot(313)  # Создание третьего подграфика
    plt.plot(hist_v, color='r')  # Отображение гистограммы для компонента V
    plt.xlim([0, 256])  # Установка диапазона отображения по оси X
    plt.show()  # О

root = tk.Tk()
root.title("Интерфейс программы")

img_label = tk.Label(root, text="Код для вставки изображения")
img_label.pack(pady=10)

btn_open_image = tk.Button(root, text="Открыть изображение", command=open_image)
btn_open_image.pack(pady=10)

root.mainloop()

tk.Tk.dia