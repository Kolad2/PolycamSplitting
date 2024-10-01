import json
import os
import zipfile
from os.path import basename
from pathlib import Path
import sys
from scipy.cluster.vq import kmeans as scipy_kmeans
from scipy.spatial import distance
import numpy as np


def make_directories(directories):
    for directory in directories:
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass
        except Exception as e:
            print(f"Ошибка при создании папок: {e}")

def find_subfolder(root_folder, target_name):
    root_path = Path(root_folder)
    for subfolder in root_path.rglob('*'):
        if subfolder.name == target_name and subfolder.is_dir():
            return subfolder
    return None

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as j_file:
        return json.load(j_file)


def is_point_in_bounding_box(point, bounding_box):
    ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = bounding_box
    x, y, z = point
    in_x = (min_x is None or x >= min_x) and (max_x is None or x <= max_x)
    in_y = (min_y is None or y >= min_y) and (max_y is None or y <= max_y)
    in_z = (min_z is None or z >= min_z) and (max_z is None or z <= max_z)
    return in_x and in_y and in_z

class ProgresBar:
    def __init__(self, total, length=40):
        self.iteration = 0
        self.total = total
        self.length = length
        progress_bar(0, self.total, self.length)

    def next_iteration(self):
        self.iteration += 1
        progress_bar(self.iteration, self.total, self.length)

def progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}%')
    sys.stdout.flush()

def plot_sphere(ax, pos, radius=1):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))*radius + pos[0]
    y = np.outer(np.sin(u), np.sin(v))*radius + pos[1]
    z = np.outer(np.ones(np.size(u)), np.cos(v))*radius + pos[2]
    # Отображаем сферу с прозрачностью
    ax.plot_surface(x, y, z, color='b', alpha=0.1)  # alpha

def kmeans(poses, k):
    centers, distortion = scipy_kmeans(poses, k)
    # Вычисление матрицы расстояний
    dist_matrix = distance.cdist(centers, centers)
    # Убираем расстояния до самой себя (должны быть равны 0)
    np.fill_diagonal(dist_matrix, np.inf)
    min_distance = np.min(dist_matrix, axis=1)
    radii = min_distance
    return centers, radii


def zip_folder(folder_path, zip_file_path):
    # Создаем ZIP-архив
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Проходим по всем файлам и папкам в указанной папке
        print("Compress process.")
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = str(os.path.join(root, file))
                relative_path = str(os.path.relpath(file_path, folder_path))
                zip_file.write(file_path, relative_path)
        print("Compress process done")




def unzip(zip_file_path):
    zip_dir = os.path.dirname(zip_file_path)
    base_name = os.path.basename(zip_file_path)
    zip_name = os.path.splitext(base_name)[0]
    zip_extension = os.path.splitext(base_name)[-1]
    if zip_extension != '.zip':
        return -1
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        folder_to_unzip = zip_dir + "/" + zip_name
        print("start unzip")
        zip_ref.extractall(folder_to_unzip)
        print("end unzip")
        return folder_to_unzip




