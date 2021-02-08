import open3d as o3d 
import numpy as np 
import glob
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing
# sdf_file = "1a04e3eab45ca15dd86060f189eb133.sdf"
ROOT_PATH = r"D:\plane_sdf\02691156_obj\02691156_obj"

def get_obj_files():
    files = glob.glob("%s/*.sdf" % ROOT_PATH, recursive=True)
    return files

def generate_data(sdf_path):
    # generate testing points
    with open(sdf_path, "r") as f:
        lines = f.readlines()

    voxel_dim = [int(i) for i in lines[0].strip().split(" ")]
    real_dim = [float(i) for i in lines[1].strip().split(" ")]
    voxel_size = float(lines[2].strip())
    points = []

    for k in range(voxel_dim[-1]):
        for j in range(voxel_dim[-2]):
            for i in range(voxel_dim[-3]):
                points.append([i*voxel_size + real_dim[0], j*voxel_size + real_dim[1], k*voxel_size + real_dim[2]])

    points = np.asarray(points)
    sdfs = [float(i.strip()) for i in lines[3:]]
    sdfs = np.asarray(sdfs)
    samples = np.concatenate([points, np.expand_dims(sdfs, axis=-1)], axis=-1)
    # get_surface_points
    surface_pcd = o3d.io.read_point_cloud(sdf_path.replace(".sdf", ".ply"))
    surface_points = np.asarray(surface_pcd.points)
    np.save(sdf_path.replace(".sdf", ".npy"), {"surface": surface_points, "sample":samples})


if __name__ == "__main__":
    files = get_obj_files()
    pool = Pool(16)
    for _ in tqdm(pool.imap_unordered(generate_data, files), total=len(files)):
        pass
    pool.close()
    pool.join()

    # generate_data(sdf_file)
    # npy_file = "1a04e3eab45ca15dd86060f189eb133.npy"
    # data = np.load(npy_file, allow_pickle=True)
    # samples = data.item()["sample"]
    # surface = data.item()["surface"]

    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(surface)

    # pcd_sampels = o3d.geometry.PointCloud()
    # pcd_sampels.points = o3d.utility.Vector3dVector(samples[:,:3][samples[:,-1]<0])
    # pcd_sampels.colors = o3d.utility.Vector3dVector(np.zeros(np.asarray(pcd_sampels.points).shape))

    # o3d.visualization.draw_geometries([pcd, pcd_sampels])