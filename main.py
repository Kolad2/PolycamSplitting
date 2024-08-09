import numpy
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import tools
from polycam_root import PolycamRoot




keyframes_folder = "/media/kolad/HardDisk/LiDAR/Horga4/Horga4-poly"
keyframes_folder_2 = "/media/kolad/HardDisk/LiDAR/Horga4/Horga4-poly_2"

polycam_root = PolycamRoot(keyframes_folder)
poses = polycam_root.poses
centers, radii = tools.kmeans(poses, 21)

i = 0
for center, radius in zip(centers, radii):
	bbox_min = center - radius
	bbox_max = center + radius
	bbox = np.vstack((bbox_min, bbox_max)).T
	polycam_root.recompile_to(str(keyframes_folder + "_" + str(i)), bbox=bbox)
	i += 1
	#exit()



exit()
sub_polycams = []
for i in range(21):
	polycam_root.recompile_to(keyframes_folder + "_" + str(i))

# polycam_2 = PolycamRoot(keyframes_folder)
#
# new_bbox = np.array([[-1.5, 2],[-0.5, 5],[None, None]])
#
#
# polycam_2.set_bbox(new_bbox)
#
#
#
# poses_2 = polycam_2.poses
#
#
#
#
# print(centers, radii)
#
# fig = plt.figure(figsize=(8, 6))  # Устанавливаем размер графика
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(poses[:, 0], poses[:, 1], poses[:, 2], color='blue', marker='.')  # Строим точки
# ax.scatter(poses_2[:,0], poses_2[:, 1], poses_2[:, 2], color='red', marker='o')  # Строим точки
# ax.scatter(centers[:,0],centers[:,1],centers[:,2], color="black", marker='o')
# # for center, radius in zip(centers, radii):
# # 	tools.plot_sphere(ax, center, radius)
#
# plt.title('Набор точек')  # Заголовок графика
# plt.xlabel('Ось X')  # Подпись оси X
# plt.ylabel('Ось Y')  # Подпись оси Y
# plt.show()  # Отображаем график