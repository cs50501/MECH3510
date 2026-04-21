from skimage import measure
import numpy as np
import matplotlib.pyplot as plt


def visualize_sphere(R):
    x, y, z = np.mgrid[-1:1:51j, -1:1:51j, -1:1:51j]
    vol = x**2 + y**2 + z**2 - R
    
    spacing = (0.04, 0.04, 0.04)
    verts, faces, normals, values = measure.marching_cubes(vol, 0, spacing = spacing)
    verts = verts - np.array([1, 1, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = "3d")
    ax.plot_trisurf(verts[:,0], verts[:,1], faces, verts[:,2])
    
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([1, 1, 1])
    
    plt.show()
    

def main():
    visualize_sphere(1)

if __name__ == "__main__":
    main()