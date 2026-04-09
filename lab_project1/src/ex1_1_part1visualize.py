import os
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot


def plot_mesh(mesh_obj, window_title, title, edgecolor = "k", alpha = 0.7):
    fig = pyplot.figure()
    fig.canvas.manager.set_window_title(window_title)
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(
        mplot3d.art3d.Poly3DCollection(
            mesh_obj.vectors,
            alpha = alpha,
            edgecolor = edgecolor
        )
    )
    
    scale = mesh_obj.points.flatten()
    ax.auto_scale_xyz(scale, scale, scale)
    ax.set_title(title)
    return fig, ax


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
    
    # Exercise 1-1 (1)   
    plot_mesh(tessa_mesh, "Ex 1-1 (1) - Tessa Vase", "Ex 1-1 (1) - Tessa Vase", edgecolor="k")
    plot_mesh(twisted_mesh, "Ex 1-1 (1) Twisted Vase", "Ex 1-1 (1) Twisted Vase", edgecolor="r")
    
    pyplot.show()


if __name__ == "__main__":
    main()