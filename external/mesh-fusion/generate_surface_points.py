import open3d as o3d 
import numpy as numpy
import glob
import os
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing

OUTPUT_PATH = "/home/daxuan/Dataset/off_files"

def get_obj_files(category):
    files = glob.glob("%s/%s_obj/*.obj" % (OUTPUT_PATH, category), recursive=True)
    return files

def sample_obj(file_path):
    if os.path.exists(os.path.join(OUTPUT_PATH, get_obj_file_name(file_path))):
        return
    print(file_path)
    mesh_obj = o3d.io.read_triangle_mesh(file_path)
    points = mesh_obj.sample_points_poisson_disk(10000)
    pcd = o3d.geometry.PointCloud()
    pcd.points = points.points
    o3d.io.write_point_cloud(get_obj_file_name(file_path), pcd)

def get_obj_file_name(file_path):
    return file_path.replace(".obj", ".ply")

if __name__ == "__main__":
    # categories = ["02691156", "02933112", "03001627", "03636649", "04090263", "04379243", "04530566", "02828884", "02958343", "03211117", "03691459", "04256520", "04401088"]
    categories = ["02691156"]

    files = []
    for category in categories:
        files += get_obj_files(category)

    pool = Pool(40)
    for _ in tqdm(pool.imap_unordered(sample_obj, files), total=len(files)):
        pass
    pool.close()
    pool.join()
