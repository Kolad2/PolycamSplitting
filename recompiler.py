from audioop import error
import os
import numpy as np
import shutil
from . import tools
from .polycam_root import PolycamRoot

def recompile(zip_root, recompile_folder=None,k=21):
	unzip_folder = tools.unzip(zip_root)
	polycam_root = PolycamRoot(unzip_folder)
	zip_dir = os.path.dirname(zip_root)
	if recompile_folder is None:
		recompile_folder = zip_dir
	elif not (os.path.exists(recompile_folder) and
	          os.path.isdir(recompile_folder)):
		raise FileNotFoundError("Файл не существует")

	zip_name = os.path.splitext(os.path.basename(zip_root))[0]
	centers, radii = tools.kmeans(polycam_root.poses, k)
	i = 0
	for center, radius in zip(centers, radii):
		bbox_min = center - radius
		bbox_max = center + radius
		bbox = np.vstack((bbox_min, bbox_max)).T
		new_folder = str(recompile_folder + "/" + zip_name + "_" + str(i))
		polycam_root.recompile_to(new_folder, bbox=bbox)
		i += 1
	# shutil.rmtree(unzip_folder)