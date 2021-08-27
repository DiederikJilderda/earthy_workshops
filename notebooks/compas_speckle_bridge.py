# basic libraries
import numpy as np

# computational geometry libraries
from compas.datastructures import Mesh as CompasMesh
from compas_plotters.meshplotter import MeshPlotter

# libraries for connection to grasshopper (speckle)
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Base, Box, Interval, Vector, Point, Plane

def speckle_to_vertices_and_faces(speckle_mesh):
    # unwrap the mesh data
    base_dict = speckle_mesh.dict()
    if "@data" in base_dict.keys():
        speckle_mesh_dict = base_dict["@data"][0][0]
    else:
        speckle_mesh_dict = base_dict


    V = np.array(speckle_mesh_dict["vertices"]).reshape((-1, 3))
    F = np.array(speckle_mesh_dict["faces"]).reshape((-1, 4))[:, 1:]

    return (V, F)

def speckle_to_compas(speckle_mesh):
    (V, F) = speckle_to_vertices_and_faces(speckle_mesh)
    compas_mesh = CompasMesh.from_vertices_and_faces(V,F)

    return compas_mesh

def compas_to_speckle(compas_mesh):
    (V, F) = compas_mesh.to_vertices_and_faces()
    (V_arr, F_arr) = (np.array(V), np.array(F))
    F_arr = np.pad(F_arr, ((0,0),(1,0)), mode='constant', constant_values=0)

    base_plane = Plane(
        origin=Point(x=0, y=0, z=0), 
        xdir= Vector(x=1, y=0, z=0), 
        ydir= Vector(x=0, y=1, z=0),
        normal= Vector(x=0, y=0, z=1))
    
    bounding_box = Box(
        basePlane = base_plane,
        area = 1,
        volume = 1,
        xSize = Interval(start=V_arr[:,0].min(), end=V_arr[:,0].max()), 
        ySize = Interval(start=V_arr[:,1].min(), end=V_arr[:,1].max()), 
        zSize = Interval(start=V_arr[:,2].min(), end=V_arr[:,2].max()))

    speckle_mesh = SpeckleMesh(
        vertices = V_arr.flatten().tolist(), 
        faces = F_arr.flatten().tolist(),
        # colors = [],
        # area = 0,
        # volume = 1,
        bbox = bounding_box
        )

    speckle_wrapped_mesh = Base(
        data = [[speckle_mesh]]
    )
    return speckle_wrapped_mesh