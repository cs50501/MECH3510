import os
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot


def rotate_method1(mesh_obj):
    

    
def rotate_method2(mesh_obj):
    




def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # get the stl of the two files, make sure they're in the same folder as this
    # i will include it in the zip folder submitted
    
    tessa_path = os.path.join(script_dir, "tessa_vase_filled-2.stl")
    twisted_path = os.path.join(script_dir, "Twisted_Vase_Basic_Voronoi_Style-1.stl")
    
    
    # get the mesh
    
    tessa_mesh = mesh.Mesh.from_file(tessa_path)
    twisted_mesh = mesh.Mesh.from_file(twisted_path)
    
    
    rotate_method1
    
    
    rotate_method2(tessa_mesh)
    rotate_method2(twisted_mesh)
    
    
if __name__ == "__main__":
    main()