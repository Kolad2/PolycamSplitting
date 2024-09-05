import os
import numpy as np
from . import tools
from .tools import load_json, find_subfolder, is_point_in_bounding_box
import shutil

class Camera:
    def __init__(self, jd):
        self.name = jd["timestamp"]
        self.cx = jd["cx"]
        self.cy = jd["cy"]
        self.matrix = np.array([
            [jd["t_00"], jd["t_01"], jd["t_02"], jd["t_03"]],
            [jd["t_10"], jd["t_11"], jd["t_12"], jd["t_13"]],
            [jd["t_20"], jd["t_21"], jd["t_22"], jd["t_23"]],
            [0.0, 0.0, 0.0, 1.0]
        ])

    @property
    def pos(self):
        return self.matrix[0:3, 3]

class PolycamRoot:
    def __init__(self, path, do_new=False):
        if do_new:
            if os.path.exists(path) and os.path.isdir(path):
                shutil.rmtree(path)
            self.make_package_folders(path)
        self.keyframes_folder = find_subfolder(path, "keyframes")
        if self.keyframes_folder is None:
            raise print("Error")
        self.keyframes_folder = str(self.keyframes_folder)
        self.package_folder = os.path.normpath(self.keyframes_folder + "/..")
        print(self.package_folder)
        self.json_folder = self.keyframes_folder + "/" + "cameras"
        self.confidence_folder = self.keyframes_folder + "/" + "confidence"
        self.depth_folder = self.keyframes_folder + "/" + "depth"
        self.images_folder = self.keyframes_folder + "/" + "images"
        self._cameras = None
        self._bbox = None
        self._poses = None

    def to_default_properties(self):
        self._bbox = None
        self._poses = None

    @property
    def cameras(self):
        if self._cameras is not None:
            return self._cameras
        cameras = []
        filenames = os.listdir(self.json_folder)
        for filename in filenames:
            filepath = self.json_folder + "/" + filename
            data = load_json(filepath)
            camera = Camera(data)
            cameras.append(camera)
        self._cameras = cameras
        return cameras

    @property
    def poses(self):
        if self._poses is not None:
            return self._poses
        poses = []
        for camera in self.cameras:
            poses.append(camera.pos)
        self._poses = np.array(poses)
        return self._poses

    @property
    def bbox(self):
        if self._bbox is not None:
            return self._bbox
        if len(self.cameras)<3:
            raise print("error")
        poses = self.poses
        self._bbox = np.array([
            [np.min(poses[:, 0]), np.max(poses[:, 0])],
            [np.min(poses[:, 1]), np.max(poses[:, 1])],
            [np.min(poses[:, 2]), np.max(poses[:, 2])],
        ])
        return self._bbox

    def set_bbox(self, bbox):
        new_cameras = []
        print(len(self.cameras))
        for pos, camera in zip(self.poses, self.cameras):
            if is_point_in_bounding_box(pos, bbox):
                new_cameras.append(camera)
        self._cameras = new_cameras
        print(len(self.cameras))
        self.to_default_properties()

    def make_package_folders(self, path, package_name=None):
        path = os.path.normpath(path)
        if package_name is None:
            package_name = os.path.basename(path)
            path = os.path.dirname(path)
        if not (os.path.exists(path) or os.path.isdir(path)):
            raise print("error")
        path = path + "/" + package_name
        new_keyframes_folder = path + "/keyframes"
        new_json_folder = new_keyframes_folder + "/cameras"
        new_images_folder = new_keyframes_folder + "/images"
        new_depth_folder = new_keyframes_folder + "/depth"
        new_confidence_folder = new_keyframes_folder + "/confidence"
        tools.make_directories([
            path,
            new_keyframes_folder,
            new_json_folder,
            new_images_folder,
            new_depth_folder,
            new_confidence_folder
        ])

    def recompile_to(self, path, bbox=None, package_name=None):
        if self.package_folder != path:
            new_root = PolycamRoot(path, do_new=True)
            new_root._cameras = self.cameras.copy()
            new_root._bbox = self.bbox.copy()
            new_root._poses = self.poses.copy()
        else:
            raise print("error")
        if bbox is not None:
            new_root.set_bbox(bbox)
        print("Recompile process:")
        bar = tools.ProgresBar(len(new_root.cameras),50)
        for camera in new_root.cameras:
            bar.next_iteration()
            shutil.copy(self.json_folder + "/" + str(camera.name) + ".json", new_root.json_folder)
            shutil.copy(self.images_folder + "/" + str(camera.name) + ".jpg", new_root.images_folder)
            shutil.copy(self.depth_folder + "/" + str(camera.name) + ".png", new_root.depth_folder)
            shutil.copy(self.confidence_folder + "/" + str(camera.name) + ".png", new_root.confidence_folder)
        print()
        tools.zip_folder(new_root.package_folder, new_root.package_folder + ".zip")

        print(self.package_folder)
        #
        return new_root

    def __del__(self):
        shutil.rmtree(self.package_folder)
        # print("Объект MyClass удален")



