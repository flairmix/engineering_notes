import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_3d_vectors(vectors, 
                   figsize=(10, 8),
                   title="3D Vector Field",
                   xlabel="X", ylabel="Y", zlabel="Z",
                   show_grid=True,
                   arrow_color="tab:blue",
                   arrow_alpha=0.8,
                   arrow_length=1.0,
                   view_elev=20, view_azim=45):
    """
    Строит 3D-график векторов с улучшенной визуализацией.
    
    Параметры:
    - vectors: массив формы (N, 6) — [[x, y, z, u, v, w], ...]
    - figsize: размер фигуры
    - title: заголовок графика
    - xlabel, ylabel, zlabel: подписи осей
    - show_grid: показывать сетку
    - arrow_color: цвет векторов
    - arrow_alpha: прозрачность векторов
    - arrow_length: масштаб длины стрелок
    - view_elev, view_azim: угол обзора (elevation, azimuth)
    """
    # Распаковка координат
    X, Y, Z, U, V, W = zip(*vectors)
    
    # Создание фигуры и оси
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    # Построение векторов (квиверов)
    quiver = ax.quiver(X, Y, Z, U, V, W,
                       color=arrow_color,
                       alpha=arrow_alpha,
                       length=arrow_length,
                       normalize=False,
                       arrow_length_ratio=0.15)  # Размер головки стрелки
    
    # Настройка пределов осей
    ax.set_xlim([0, max(X) + 2])
    ax.set_ylim([0, max(Y) + 2])
    ax.set_zlim([0, max(Z) + 3])
    
    # Подписи и заголовок
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_zlabel(zlabel, fontsize=12)
    ax.set_title(title, fontsize=14, pad=20)
    
    # Сетка и стиль
    ax.grid(show_grid)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    
    # Угол обзора
    ax.view_init(elev=view_elev, azim=view_azim)
    
    plt.tight_layout()
    plt.show()
    return fig, ax



