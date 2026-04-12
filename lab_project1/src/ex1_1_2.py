import os
import math
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot


def plot_comparison(original_mesh, rotated_mesh, window_title, title):
    fig = pyplot.figure()
    fig.canvas.manager.set_window_title(window_title)
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(
        mplot3d.art3d.Poly3DCollection(
            original_mesh.vectors,
            alpha = 0.3,
            edgecolor = "k"
        )
    )
    ax.add_collection3d(
        mplot3d.art3d.Poly3DCollection(
            rotated_mesh.vectors,
            alpha = 0.3,
            edgecolor = "r"
        )
    )
    
    scale = np.concatenate(
        [original_mesh.points.flatten(), rotated_mesh.points.flatten()]
    )
    ax.auto_scale_xyz(scale, scale, scale)
    ax.set_title(title + " (black = original, red = rotated)")


def rotate_method1(mesh_obj):
    rotated_mesh = mesh.Mesh(mesh_obj.data.copy())
    
    
    theta_x = -math.pi / 4
    theta_y = math.pi / 3
    
    
    rot_x = np.array([
        [1, 0, 0],
        [0, math.cos(theta_x), -math.sin(theta_x)],
        [0, math.sin(theta_x), math.cos(theta_x)]
    ])
    
    
    rot_y = np.array([
        [math.cos(theta_y), 0, math.sin(theta_y)],
        [0, 1, 0],
        [-math.sin(theta_y), 0, math.cos(theta_y)]
    ])
    
    
    for i in range(len(rotated_mesh.vectors)):
        for j in range(3):
            v = rotated_mesh.vectors[i][j]
            v = rot_x @ v
            v = rot_y @ v
            rotated_mesh.vectors[i][j] = v

    return rotated_mesh


    
def rotate_method2(mesh_obj):
    rotated_mesh = mesh.Mesh(mesh_obj.data.copy())
    
    
    rotated_mesh.rotate([1, 0, 0], math.pi / 4)
    rotated_mesh.rotate([0, 1, 0], -math.pi / 3)
    
    
    return rotated_mesh


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, "data")
    
    # get the stl of the two files, make sure they're in the same folder as this
    # i will include it in the zip folder submitted
    tessa_path = os.path.join(data_dir, "tessa_vase_filled-2.stl")
    twisted_path = os.path.join(data_dir, "Twisted_Vase_Basic_Voronoi_Style-1.stl")
    
    
    # get the mesh
    tessa_mesh = mesh.Mesh.from_file(tessa_path)
    twisted_mesh = mesh.Mesh.from_file(twisted_path)
    
    
    tessa_rot1 = rotate_method1(tessa_mesh)
    twisted_rot1 = rotate_method1(twisted_mesh)
    
    
    tessa_rot2 = rotate_method2(tessa_mesh)
    twisted_rot2 = rotate_method2(twisted_mesh)
    
    
    plot_comparison(tessa_mesh, tessa_rot1, "Exercise 1-1 (2) Tessa Vase - Method 1", "Tessa Vase - Method 1")
    plot_comparison(twisted_mesh, twisted_rot1, "Exercise 1-1 (2) Twisted Vase - Method 1", "Twisted Vase - Method 1")
    
    plot_comparison(tessa_mesh, tessa_rot2, "Exercise 1-1 (2) Tessa Vase - Method 2", "Tessa Vase - Method 2")
    plot_comparison(twisted_mesh, twisted_rot2, "Exercise 1-1 (2) Twisted Vase - Method 2", "Twisted Vase - Method 2")
    
    pyplot.show()
    
    
if __name__ == "__main__":
    main()