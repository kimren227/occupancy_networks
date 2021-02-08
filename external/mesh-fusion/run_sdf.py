import open3d as o3d 
import numpy as numpy
import glob
import os
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing

MESH_ROOT="/home/daxuan/Dataset/off_files/02691156_water_tight"
MESH_OBJ_ROOT="/home/daxuan/Dataset/off_files/02691156_obj"

# categories = ["02691156", "02933112", "03001627", "03636649", "04090263", "04379243", "04530566", "02828884", "02958343", "03211117", "03691459", "04256520", "04401088"]
categories = ["02691156"]

def get_off_files(mesh_root):
    files = glob.glob("%s/*.off" % mesh_root, recursive=True)
    return files

def get_obj_files(mesh_obj_root):
    files = glob.glob("%s/*.obj" % mesh_obj_root, recursive=True)
    return files

def convert_off_obj(file_path):
    if os.path.exists(file_path.replace("water_tight", "obj").replace(".off", ".obj")):
        return
    mesh_off = o3d.io.read_triangle_mesh(file_path)
    mesh_obj = o3d.geometry.TriangleMesh()
    mesh_obj.vertices = mesh_off.vertices
    mesh_obj.triangles = mesh_off.triangles
    o3d.io.write_triangle_mesh(file_path.replace("water_tight", "obj").replace(".off", ".obj"), mesh_obj)

def run_sdf(file_path):
    print("./SDFGen %s 0.005 1" % file_path)
    os.system("./SDFGen %s 0.005 1" % file_path)

if __name__ == "__main__":

    for category in categories:
    
        files = get_off_files(MESH_ROOT.replace("02691156", category))
        pool = Pool(40)
        for _ in tqdm(pool.imap_unordered(convert_off_obj, files), total=len(files)):
            pass
        pool.close()
        pool.join()

        files = get_obj_files(MESH_OBJ_ROOT.replace("02691156", category))
        pool = Pool(4)
        for _ in tqdm(pool.imap_unordered(run_sdf, files), total=len(files)):
            pass
        pool.close()
        pool.join()