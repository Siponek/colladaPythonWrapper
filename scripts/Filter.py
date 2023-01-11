import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)
import collada as cl
from libs import colladaWraperLib as clw
import numpy as np


def main(*args, **kwargs):
    """Main funtion for reading, preparing objects, applying transformations, saving to file"""

    path_to_file : Path = Path("data/cubes_scene.dae")
    path_to_save : Path = Path("data/cubes_scene_filtered.dae")

    with open(file=path_to_file, mode="rb") as cubes_scene_file:
        mesh = cl.Collada(cubes_scene_file)
        mesh.assetInfo.upaxis = "Z_UP"
        print(f"This is the whole scene source list object \t\t{mesh}")
        print(f"This is the first geometry object \t\t\t{mesh.geometries[0]}")
        print(
            f"This is the first scene node object \t\t\t{mesh.scene.nodes[0]}" 
        )
        new_scene_mesh = cl.Collada()
        # ? Chaning the list_to_pick_from to quickly test out the fucntions
        list_to_pick_from = clw.filter_by_uniform_area(scene=mesh.scene, upper_bound=15)
        new_scene_mesh.assetInfo.upaxis = "Z_UP"
        new_scene_mesh = clw.prepare_collada_obj(
            new_scene_mesh,
            mesh,
            list_to_pick_from=list_to_pick_from,
            verbose=False,
        )
        origin_point : np.ndarray = clw.mean_of_centre(list_to_pick_from)
        origin_point_negative : np.ndarray = np.negative(origin_point)

        # ? Transformation Part
        clw.apply_transformation(
            scene=new_scene_mesh.scene,
            transform_offsetX=origin_point_negative[0],
            transform_offsetY=origin_point_negative[1],
            transform_offsetZ=origin_point_negative[2],
        )

        clw.apply_transformation(
            scene=new_scene_mesh.scene,
            pivot_of_rotation=[0, 0, 1],
            degrees_to_rotate=30,
        )

        clw.apply_transformation(
            scene=new_scene_mesh.scene,
            transform_offsetX=origin_point[0],
            transform_offsetY=origin_point[1],
            transform_offsetZ=origin_point[2],
        )
        clw.apply_transformation(
            scene=new_scene_mesh.scene,
            transform_offsetY=20,
        )
        print(f"Saving output to _> {path_to_save}")
        new_scene_mesh.write(path_to_save)


if __name__ == "__main__":
    main()
