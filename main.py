


keyframes_folder = "/media/kolad/HardDisk/LiDAR/Horga4/Horga4-poly"

zip_file = "/media/kolad/HardDisk/LiDAR/Horga4.zip"

pack_folder = "/media/kolad/HardDisk/LiDAR/PackFolder"

recompile(zip_file,pack_folder)

# polycam_recompile(zip_file)


# fig = plt.figure(figsize=(8, 6))  # Устанавливаем размер графика
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(poses[:, 0], poses[:, 1], poses[:, 2], color='blue', marker='.')  # Строим точкиоим точки
# ax.scatter(centers[:,0],centers[:,1],centers[:,2], color="black", marker='o')
# for center, radius in zip(centers, radii):
# 	tools.plot_sphere(ax, center, radius)
#
# plt.title('Набор точек')  # Заголовок графика
# plt.xlabel('Ось X')  # Подпись оси X
# plt.ylabel('Ось Y')  # Подпись оси Y
# plt.show()  # Отображаем график