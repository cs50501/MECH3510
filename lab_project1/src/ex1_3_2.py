from skimage import measure
import numpy as np
import matplotlib.pyplot as plt


def box_field(x, y, z):
    return np.maximum.reduce([
        np.abs(x) - 0.5,
        np.abs(y) - 0.5,
        np.abs(z) - 0.5
    ])


def cylinder_field(x, y, z):
    r = 0.1

    radial = x**2 + y**2 - r**2
    slab = np.maximum(0.5 - z, z - 0.7)

    return np.maximum(radial, slab)


def union_minmax(f1, f2):
    return np.minimum(f1, f2)


def union_r(f1, f2, alpha):
    return (f1 + f2 - np.sqrt(f1**2 + f2**2 - 2*alpha*f1*f2)) / (1 + alpha)


def visualize_union(method="minmax"):
    n = 301
    x, y, z = np.mgrid[-1:1:complex(n), -1:1:complex(n), -1:1:complex(n)]

    f_box = box_field(x, y, z)
    f_cyl = cylinder_field(x, y, z)

    if method == "minmax":
        vol = union_minmax(f_box, f_cyl)
        title = "Union using min/max"
    elif method == "r":
        vol = union_r(f_box, f_cyl, 0)
        title = "Union using R-function"
    else:
        raise ValueError("method must be 'minmax' or 'r'")

    spacing = (2/(n-1), 2/(n-1), 2/(n-1))
    verts, faces, normals, values = measure.marching_cubes(vol, 0, spacing=spacing)

    # shift coordinates from [0,2] back to [-1,1]
    verts = verts - np.array([1, 1, 1])

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], linewidth=0.15)

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([1, 1, 1])


def main():
    visualize_union("minmax")
    visualize_union("r")
    
    
    plt.show()


if __name__ == "__main__":
    main()