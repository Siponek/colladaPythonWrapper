import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)
from libs.colladaWraperLib import *


def main():
    """Main funtion from reading, preparing objects, applying transformations, saving to file"""

    pathToFile: str = ".\data\\" + "cubes_scene.dae"
    pathToSave: str = ".\data\\" + "cubes_scene_filtered.dae"

    with open(file=pathToFile, mode="rb") as cubesSceneFile:
        mesh = cl.Collada(cubesSceneFile)
        ##   ,
        ##   ignore=[cl.common.DaeUnsupportedError, cl.common.DaeBrokenRefError]
        mesh.assetInfo.upaxis = "Z_UP"
        print("This is the whole scene source list object \t\t", mesh)
        print("This is the first geometry object \t\t\t", mesh.geometries[0])
        print(
            "This is the first scene node object \t\t\t", mesh.scene.nodes[0]
        )

        newSceneMesh = cl.Collada()
        # ? Chaning the listToPickFrom to quickly test out the fucntions

        # listToPickFrom = filterByMaterial(scene=mesh.scene, verbose=False)

        # listToPickFrom = filterByMaterial(
        #     scene=mesh.scene, materialName="Material.002"
        # )

        listToPickFrom = filterByUniformArea(scene=mesh.scene, upper_bound=15)

        newSceneMesh = prepareColladaObj(
            newSceneMesh,
            mesh,
            listToPickFrom=listToPickFrom,
            verbose=False,
        )
        newSceneMesh.assetInfo.upaxis = "Z_UP"
        originPoint = meanOfCentre(listToPickFrom)
        originPoint_negative = np.negative(originPoint)

        # ? Transformation Part
        applyTransformation(
            scene=newSceneMesh.scene,
            transform_offsetX=originPoint_negative[0],
            transform_offsetY=originPoint_negative[1],
            transform_offsetZ=originPoint_negative[2],
        )

        applyTransformation(
            scene=newSceneMesh.scene,
            pivotOfRotation=[0, 0, 1],
            degreesToRotate=30,
        )

        applyTransformation(
            scene=newSceneMesh.scene,
            transform_offsetX=originPoint[0],
            transform_offsetY=originPoint[1],
            transform_offsetZ=originPoint[2],
        )
        applyTransformation(
            scene=newSceneMesh.scene,
            transform_offsetY=20,
        )
        print(f"Saving output to _> {pathToSave}")
        newSceneMesh.write(pathToSave)


if __name__ == "__main__":
    main()
