import open3d as o3d
import open3d.visualization.rendering as rendering
import numpy as np
import os, sys


def render_image(path, name):
    print("current mesh:", path+"/"+name)
    mesh = o3d.io.read_triangle_mesh(path+"/"+name)
    mesh.compute_vertex_normals()

    R = mesh.get_rotation_matrix_from_axis_angle([-(np.pi / 2), 0, 0])  # radians
    mesh.rotate(R, center=mesh.get_center())

    material = rendering.MaterialRecord()
    material.shader = "defaultLit"

    width, height = 800, 600
    renderer = rendering.OffscreenRenderer(width, height)

    scene = renderer.scene
    scene.set_background([1.0, 1.0, 1.0, 1.0])  # White background
    scene.add_geometry("mesh", mesh, material)

    bbox = mesh.get_axis_aligned_bounding_box()
    center = bbox.get_center()
    extent = bbox.get_extent().max()

    # Set up the camera
    cam = scene.camera
    eye = center + [0, 0, extent]  # Camera position (in front of object)
    lookat = center  # Where the camera looks
    up = [0, 1, 0]  # Up direction

    cam.look_at(lookat, eye, up)

    image = renderer.render_to_image()
    o3d.io.write_image("images/" + name.split('.')[0]+".png", image)

def main():
    print("getting STL's")
    if not os.path.isdir(sys.argv[1]):
        print("Not a valid path")
        return
    
    arr = os.listdir(sys.argv[1])
    print(arr)
    stls =  [p for p in arr if p.endswith('.stl')]
    count = 0
    for stl in stls:
        render_image(sys.argv[1], stl)
        count += 1
        print(count , "/" , len(stls))

main()

