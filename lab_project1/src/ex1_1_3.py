import os
import math
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
    
    
def compare_area_results(mesh_obj, model_name):
    area1 = surface_area_method1(mesh_obj)
    area2 = surface_area_method2(mesh_obj)
    
    
    abs_diff = abs(area1 - area2)
    percent_diff = abs_diff / area1 * 100
    
    print(f"\n{model_name}")
    print("-" * len(model_name))
    print(f"Method 1 (Cross Product): {area1:.6f}")
    print(f"Method 2 (mesh.areas): {area2:.6f}")
    print(f"Absolute Difference: {abs_diff:.10f}")
    print(f"Percentage Difference: {percent_diff:.10f}%")
    
    
def surface_area_method1(mesh_obj):
    total_area = 0.0
    
    for triangle in mesh_obj.vectors:
        p0 = triangle[0]
        p1 = triangle[1]
        p2 = triangle[2]
        
        edge1 = p1 - p0
        edge2 = p2 - p0
        
        cross_product = np.cross(edge1, edge2)
        triangle_area = 0.5 * np.linalg.norm(cross_product)
        
        total_area += triangle_area
        
    return total_area


def surface_area_method2(mesh_obj):
    return np.sum(mesh_obj.areas)


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
    
    
    compare_area_results(tessa_mesh, "Tessa Vase")
    compare_area_results(twisted_mesh, "Twisted Vase")
    

if __name__ == "__main__":
    main()