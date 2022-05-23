"""Main libary package for Filter.py program by Szymon Zinkowicz
        Ponglish Version
"""
import collada as cl
import numpy as np


def filterByMaterial(
    scene,
    materialName: str = "Material.001",
    returnBlanks: bool = False,
    verbose: bool = False,
) -> list:
    """A function that returns a list of collada.geometry.BoundGeometry objects. Checks the first node of given obj.primitives() for material. Possbile to use obj.original on obj from list to rerutn not-bound geometry.
        'cl' as if collada imported as 'cl'.
        yellowMaterial = 'Material.001' ;
        blueMaterial = 'Material.002'
    Args:
        scene (cl.collada.scene, <class 'collada.scene.Scene'>): A cl.Collada object. (e.g. read from file)
        materialName (str, optional): Name of the material that cointains the required color/attribute. In case of not specifing correct string for the material name - it returns every material that is not 'Material.001'". Defaults to "Material.001".
        returnBlanks (bool, optional): If True then returns list with notbound geometry without materials (material as Nonetype). Defaults to False.

    Returns:
        list: List of collada.geometry.BoundGeometry objects with selected material
    """

    if type(scene) != cl.scene.Scene:
        print("Incorrect type as scene!")
        raise ValueError

    listOf_sceneGeoNodes = list(scene.objects("geometry"))
    if verbose == True:
        print(
            f"FUNC filterByMaterial: Amount of nodes to search though_> {len(listOf_sceneGeoNodes)}"
        )
    yellowMaterial = "Material.001"
    # Not used to bring more functionality as default "garbage collector"
    blueMaterial = "Material.002"

    listOf_yellows: list = []
    listOf_blues: list = []
    listOf_None: list = []

    for idx, obj in enumerate(listOf_sceneGeoNodes):
        geo = list(obj.primitives())
        triangle = geo[0]
        if triangle.material is None:
            listOf_None.append(obj)
            continue

        if verbose == True:
            print(triangle.material.name)
        if triangle.material.name == yellowMaterial:
            listOf_yellows.append(obj)
        else:
            listOf_blues.append(obj)

    if returnBlanks == True:
        if verbose == True:
            print(f"Returned listOf_None {len(listOf_None)} objects")
        return listOf_None
    elif materialName == yellowMaterial:
        if verbose == True:
            print(f"Returned listOf_yellows {len(listOf_yellows)} objects")
        return listOf_yellows
    else:
        if verbose == True:
            print(f"Returned listOf_blues {len(listOf_blues)} objects")
        return listOf_blues


def filterByUniformArea(
    scene,
    upper_bound: float,
    lower_bound: float = 0,
    inside: bool = True,
    verbose: bool = False,
) -> list:
    """_summary_

    Args:
        scene (_type_): _description_
        upper_bound (float): _description_
        lower_bound (float, optional): _description_. Defaults to 0.
        inside (bool, optional): _description_. Defaults to True.
        verbose (bool, optional): _description_. Defaults to False.

    Returns:
        list: _description_
    """

    listOf_inArea: list = []
    listOf_outOfBounds: list = []
    listOf_sourceGeoNodes = list(scene.objects("geometry"))

    for idx_1, obj in enumerate(listOf_sourceGeoNodes):
        geo = list(obj.primitives())
        triangle = geo[0]

        for idx_2, arrayOfVerts in enumerate(triangle.vertex):
            vertInArea = np.all(
                (lower_bound < arrayOfVerts) & (arrayOfVerts < upper_bound)
            )
            if vertInArea == True:
                listOf_inArea.append(obj)
                break
            if idx_2 == len(triangle.vertex) - 1:
                listOf_outOfBounds.append(obj)
        if verbose == True:
            print(f"This is the amount of inArea {len(listOf_inArea)}")
            print(
                f"This is the amount of outOfBounds {len(listOf_outOfBounds)}"
            )
    if inside == True:
        return listOf_inArea
    else:
        return listOf_outOfBounds


def prepareColladaObj(
    newSceneObject,
    objectToCopyFrom,
    listToPickFrom,
    nameOfTheScene: str = "myscene",
    verbose: bool = False,
):
    """_summary_

    Args:
        newSceneObject (_type_): _description_
        objectToCopyFrom (_type_): _description_
        listToPickFrom (_type_): _description_
        nameOfTheScene (str, optional): _description_. Defaults to "myscene".
        verbose (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    amountOfObjects = len(list(objectToCopyFrom.scene.objects("geometry")))
    for x_Eff in objectToCopyFrom.effects:
        newSceneObject.effects.append(x_Eff)

    for x_Mat in objectToCopyFrom.materials:
        newSceneObject.materials.append(x_Mat)

    indexOfCorrectNodes = []
    for x_Geo in listToPickFrom:
        x_Geo = x_Geo.original
        if verbose == True:
            print("x_Geo", x_Geo.name)
        indexOfCorrectNodes.append(amountOfObjects - int(x_Geo.name[-3:]))
        newSceneObject.geometries.append(x_Geo)
    compressed_nodes = [
        val
        for idx, val in enumerate(objectToCopyFrom.scene.nodes)
        if idx in indexOfCorrectNodes
    ]
    try:
        if verbose == True:
            print(compressed_nodes[0].id)
    except IndexError:
        print("Zero nodes in the selection !!!")
    myscene = cl.scene.Scene(nameOfTheScene, compressed_nodes)
    newSceneObject.scenes.append(myscene)
    newSceneObject.scene = myscene

    return newSceneObject


def meanOfCentre(listToPickFrom: list, verbose: bool = False) -> np.ndarray:
    """_summary_

    Args:
        listToPickFrom (list): _description_
        verbose (bool, optional): _description_. Defaults to True.

    Returns:
        np.ndarray: _description_
    """

    centralPoint: np.array = 0
    tmpSum = 0
    amount: int = 0
    for x_Geo in listToPickFrom:
        geo = list(x_Geo.primitives())
        triangle = geo[0]

        for idx_2, arrayOfVerts in enumerate(triangle.vertex):
            tmpSum += arrayOfVerts
            amount += 1
    if amount < 1:
        return print("THERE IS NOTHING IN THE LIST OF GEOMETRIES")
    centralPoint = tmpSum / amount

    if verbose == True:
        print("Sum of the verts:\n\t", tmpSum)
        print("Amount of the verts:\n\t", amount)
        print("Central mean of vertices:\n\t", centralPoint)

    return centralPoint


def applyTransformation(
    scene,
    pivotOfRotation=[0, 0, 0],
    transform_offsetX: float = 0,
    transform_offsetY: float = 0,
    transform_offsetZ: float = 0,
    scalevalueX: float = 1,
    scalevalueY: float = 1,
    scalevalueZ: float = 1,
    degreesToRotate: float = 0,
    verbose: bool = False,
) -> None:
    """_summary_

    Args:
        scene (_type_): _description_
        pivotOfRotation (list, optional): _description_. Defaults to [0, 0, 0].
        transform_offsetX (float, optional): _description_. Defaults to 0.
        transform_offsetY (float, optional): _description_. Defaults to 0.
        transform_offsetZ (float, optional): _description_. Defaults to 0.
        scalevalueX (float, optional): _description_. Defaults to 1.
        scalevalueY (float, optional): _description_. Defaults to 1.
        scalevalueZ (float, optional): _description_. Defaults to 1.
        degreesToRotate (float, optional): _description_. Defaults to 0.
        localTransform (bool, optional): _description_. Defaults to False.
        verbose (bool, optional): _description_. Defaults to False.
    """
    matrixScale = cl.scene.ScaleTransform(
        scalevalueX, scalevalueY, scalevalueZ
    )
    # matrixRotation = cl.scene.RotateTransform(
    #     pivotOfRotation[0],
    #     pivotOfRotation[1],
    #     pivotOfRotation[2],
    #     np.radians(degreesToRotate),
    # )

    cos = np.cos(np.radians(degreesToRotate))
    sin = np.sin(np.radians(degreesToRotate))
    x, y, z = pivotOfRotation[0], pivotOfRotation[1], pivotOfRotation[2]
    matrixRotation = np.array(
        [
            [
                (1 - cos) * x * x + cos,
                (1 - cos) * x * y - sin * z,
                (1 - cos) * x * z + sin * y,
                0,
            ],
            [
                (1 - cos) * x * y + sin * z,
                (1 - cos) * y * y + cos,
                (1 - cos) * z * y - sin * x,
                0,
            ],
            [
                (1 - cos) * x * z - sin * y,
                (1 - cos) * y * z + sin * x,
                (1 - cos) * z * z + cos,
                0,
            ],
            [0, 0, 0, 1],
        ]
    )

    matrixTranslate = cl.scene.TranslateTransform(
        transform_offsetX, transform_offsetY, transform_offsetZ
    )

    for idx, nodeX in enumerate(scene.nodes):
        transforms_old = nodeX.transforms[0]
        if verbose == True:
            print("Old_matrix _>\n", transforms_old.matrix)

        final_matrix = cl.scene.MatrixTransform(
            np.dot(
                np.dot(
                    np.dot(matrixTranslate.matrix, matrixRotation),
                    matrixScale.matrix,
                ),
                transforms_old.matrix,
            ).flatten()
        )
        scene.nodes[idx].transforms[0] = final_matrix
        (scene.nodes[idx]).save()
    if verbose == True:
        print(f"Scaling _>\n {matrixScale.matrix}")
        print(f"Rotations _>\n {matrixRotation}")
        print(f"NEW _>\n {scene.nodes[0].transforms[0].matrix}")


def zeroedCoords(
    scene,
    oldInvertedMatrix: np.ndarray = np.identity(4),
    verbose: bool = False,
) -> list:
    """_summary_

    Args:
        scene (_type_): _description_
        oldInvertedMatrix (np.ndarray, optional): _description_. Defaults to np.identity(4).
        verbose (bool, optional): _description_. Defaults to False.

    Returns:
        list: _description_
    """
    listOf_minusTranslates = []
    for idx, nodeX in enumerate(scene.nodes):
        transforms_old = nodeX.transforms[0]
        transforms_old_INV = np.linalg.inv(transforms_old.matrix)

        if verbose == True:
            print(f"Old_matrix _>\n {transforms_old.matrix}")

        final_matrix = cl.scene.MatrixTransform(oldInvertedMatrix.flatten())
        listOf_minusTranslates.append(transforms_old_INV)
        scene.nodes[idx].transforms[0] = final_matrix
        (scene.nodes[idx]).save()
        if verbose == True:
            print(f"final_matrix _>\n {final_matrix.matrix}")
    return listOf_minusTranslates


def reverseTranslation(
    scene, oldInvertedMatrix=np.identity(4), verbose: bool = False
):
    """_summary_

    Args:
        scene (_type_): _description_
        oldInvertedMatrix (_type_, optional): _description_. Defaults to np.identity(4).
        verbose (bool, optional): _description_. Defaults to False.
    """
    for idx, nodeX in enumerate(scene.nodes):
        transforms_curernt = nodeX.transforms[0]
        transforms_old_INV = np.linalg.inv(oldInvertedMatrix[idx])
        tmpArray = np.identity(4)
        tmpArray[0, 3] = transforms_old_INV[0, 3]
        tmpArray[1, 3] = transforms_old_INV[1, 3]
        tmpArray[2, 3] = transforms_old_INV[2, 3]
        if verbose == True:
            print(f"tmpArray\n {tmpArray}")
        final_matrix = cl.scene.MatrixTransform(
            np.dot(tmpArray, transforms_curernt.matrix).flatten()
        )
        scene.nodes[idx].transforms[0] = final_matrix
        (scene.nodes[idx]).save()


def reverseRotation(
    scene, oldInvertedMatrix=np.identity(4), verbose: bool = False
):
    """_summary_

    Args:
        scene (_type_): _description_
        oldInvertedMatrix (_type_, optional): _description_. Defaults to np.identity(4).
        verbose (bool, optional): _description_. Defaults to False.
    """

    for idx, nodeX in enumerate(scene.nodes):
        transforms_curernt = nodeX.transforms[0]
        transforms_old_INV = np.linalg.inv(oldInvertedMatrix[idx])
        tmpArray = np.identity(4)
        tmpArray[0][0] = transforms_old_INV[0][0]
        tmpArray[1][0] = transforms_old_INV[1][0]
        tmpArray[2][0] = transforms_old_INV[2][0]
        tmpArray[0][1] = transforms_old_INV[0][1]
        tmpArray[1][1] = transforms_old_INV[1][1]
        tmpArray[2][1] = transforms_old_INV[2][1]
        tmpArray[0][2] = transforms_old_INV[0][2]
        tmpArray[1][2] = transforms_old_INV[1][2]
        tmpArray[2][2] = transforms_old_INV[2][2]
        if verbose == True:
            print(f"tmpArray\n {tmpArray}")
        final_matrix = cl.scene.MatrixTransform(
            np.dot(tmpArray, transforms_curernt.matrix).flatten()
        )

        scene.nodes[idx].transforms[0] = final_matrix
        (scene.nodes[idx]).save()
