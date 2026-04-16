import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import marching_cubes



def psi_periodic(X, Y, Z, mu, kappa, p):
    mu = np.asarray(mu, dtype=float)
    p = np.asarray(p, dtype=float)
    
    if np.isscalar(kappa):
        kappa = np.full(len(mu), float(kappa))
    else:
        kappa = np.asarray(kappa, dtype=float)
        
    psi = np.zeros_like(X, dtype=float)
    
    for j in range(len(mu)):
        phase = p[0, j] * X + p[1, j] * Y + p[2, j] * Z + p[3, j]
        psi += mu[j] * np.cos(2.0 * np.pi * kappa[j] * phase)

    return psi


def get_surface_parameters():
    params = {}
    
    # P surface
    params["P"] = {
        "mu": np.array([1, 1, 1], dtype=float),
        "p": np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0]
        ], dtype=float)
    }
    
    # D surface
    params["D"] = {
        "mu": np.array([1, 1, 1, 1, -1, 1, 1, -1]),
        "p": np.array([
            [1, 1, 1, 1, -1, -1, -1, -1],
            [-1, -1, 1, 1, 1, 1, -1, -1],
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [0, 0, 0, 0, 1/4, 1/4, 1/4, 1/4]
        ], dtype=float)
    }
    
    # G surface
    params["G"] = {
        "mu": np.array([1, 1, 1, 1, 1, -1], dtype=float),
        "p": np.array([
            [-1, -1,  0,  0, -1, -1],
            [-1,  1, -1, -1,  0,  0],
            [ 0,  0, -1,  1, -1,  1],
            [1/4, 1/4, 1/4, 1/4, 1/4, 1/4]
        ], dtype=float)
    }
    
    return params


def create_grid(n=50, xlim=(0.0, 1.0), ylim=(0.0, 1.0), zlim=(0.0, 1.0)):
    x = np.linspace(*xlim, n)
    y = np.linspace(*ylim, n)
    z = np.linspace(*zlim, n)
    return np.meshgrid(x, y, z, indexing="ij")


def plot_isosurface(F, xlim, ylim, zlim, title):
    nx, ny, nz = F.shape
    dx = (xlim[1] - xlim[0]) / (nx - 1)
    dy = (ylim[1] - ylim[0]) / (ny - 1)
    dz = (zlim[1] - zlim[0]) / (nz - 1)

    verts, faces, _, _ = marching_cubes(F, level=0.0, spacing=(dx, dy, dz))

    # shift to actual coordinate origin
    verts[:, 0] += xlim[0]
    verts[:, 1] += ylim[0]
    verts[:, 2] += zlim[0]

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_trisurf(
        verts[:, 0], verts[:, 1], faces, verts[:, 2],
        linewidth=0.1, alpha=0.9
    )

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    ax.set_box_aspect([1, 1, 1])

    plt.tight_layout()


def main():
    # scale parameter
    kappa = 1.0
    
    # grid settings
    n = 55
    xlim = (0.0, 1.0)
    ylim = (0.0, 1.0)
    zlim = (0.0, 1.0)

    X, Y, Z = create_grid(n=n, xlim=xlim, ylim=ylim, zlim=zlim)
    surface_params = get_surface_parameters()

    for name, data in surface_params.items():
        F = psi_periodic(X, Y, Z, data["mu"], kappa, data["p"])
        plot_isosurface(F, xlim, ylim, zlim, f"{name} surface, psi = 0")

    plt.show()


if __name__ == "__main__":
    main()