import open3d as o3d 
import numpy as numpy
import glob
import os
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing

SHAPENET_ROOT="/home/daxuan/Dataset/ShapeNetCore.v2"
OUTPUT_PATH = "/home/daxuan/Dataset/off_files"

def get_shapenet_files(category):
    files = glob.glob("%s/%s/**/models/*.obj" % (SHAPENET_ROOT, category), recursive=True)
    return files

def convert_obj_off1(file_path):
    try:
        mesh_obj = o3d.io.read_triangle_mesh(file_path)
        mesh_off = o3d.geometry.TriangleMesh()
        mesh_off.vertices = mesh_obj.vertices
        mesh_off.triangles = mesh_obj.triangles
        o3d.io.write_triangle_mesh(os.path.join(OUTPUT_PATH, get_obj_file_name(file_path)), mesh_off)
    except KeyboardInterrupt:
        exit(0)
        pass
    except Exception as e:
        print("Error processing: %s" % file_path)

def convert_obj_off(file_path):
    if os.path.exists(os.path.join(OUTPUT_PATH, get_obj_file_name(file_path))):
        return
    print(file_path)
    mesh_obj = o3d.io.read_triangle_mesh(file_path)
    mesh_off = o3d.geometry.TriangleMesh()
    mesh_off.vertices = mesh_obj.vertices
    mesh_off.triangles = mesh_obj.triangles
    o3d.io.write_triangle_mesh(os.path.join(OUTPUT_PATH, get_obj_file_name(file_path)), mesh_off)

def convert_obj_off_wrapper(file_path):
    p = multiprocessing.Process(target=convert_obj_off, args=(file_path,))
    p.start()
    # Wait for 10 seconds or until process finishes
    p.join(10)
    # If thread is still active
    if p.is_alive():
        print("Killing %s" % file_path)
        p.terminate()
        p.join()

def get_obj_file_name(file_path):
    return file_path.split("/")[-4]+"/"+file_path.split("/")[-3]+".off"

if __name__ == "__main__":
    categories = ["02691156", "02933112", "03001627", "03636649", "04090263", "04379243", "04530566", "02828884", "02958343", "03211117", "03691459", "04256520", "04401088"]
    files = []
    for category in categories:
        print("Working on %s..." % category)
        if not os.path.exists(os.path.join(OUTPUT_PATH, category)):
            os.system("mkdir -p %s" % os.path.join(OUTPUT_PATH, category))
        files += get_shapenet_files(category)

    pool = Pool(40)
    for _ in tqdm(pool.imap_unordered(convert_obj_off, files), total=len(files)):
        pass
    pool.close()
    pool.join()
