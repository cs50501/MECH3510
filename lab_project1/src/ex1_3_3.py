from skimage import measure
import numpy as np
import matplotlib.pyplot as plt


def sphere_field(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2) - 1.0


def box_field(x, y, z):
    return np.maximum.reduce([
        np.abs(x) - 0.5,
        np.abs(y) - 0.5,
        np.abs(z) - 0.5
    ])


def cylinder_field(x, y, z):
    r = 0.1
    radial = x**2 + y**2 - r**2
    slab = np.maximum(0.5 - z, z - 0.7)   # restrict to 0.5 <= z <= 0.7
    return np.maximum(radial, slab)


def box_cylinder_union(x, y, z):
    f_box = box_field(x, y, z)
    f_cyl = cylinder_field(x, y, z)
    return np.minimum(f_box, f_cyl)   # min/max version only


def morph_field(x, y, z, mu):
    f_sphere = sphere_field(x, y, z)
    f_bc = box_cylinder_union(x, y, z)
    return mu * f_sphere + (1 - mu) * f_bc


def plot_isosurface(vol, n, title):
    spacing = (2/(n-1), 2/(n-1), 2/(n-1))
    verts, faces, normals, values = measure.marching_cubes(vol, 0, spacing=spacing)

    # shift coordinates from [0,2] back to [-1,1]
    verts = verts - np.array([1, 1, 1])

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], linewidth=0.1)

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect([1, 1, 1])

    # optional: keep view angle same for all screenshots
    ax.view_init(elev=20, azim=-60)

def main():
    n = 101
    x, y, z = np.mgrid[-1:1:complex(n), -1:1:complex(n), -1:1:complex(n)]

    mus = np.linspace(0, 1, 11)   # 0, 0.1, ..., 1.0

    for i, mu in enumerate(mus):
        vol = morph_field(x, y, z, mu)
        plot_isosurface(vol, n, title=f"Morph step {i} (mu={mu:.1f})")
        
    plt.show()


if __name__ == "__main__":
    main()