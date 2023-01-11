"""Main libary package for Filter.py program by Szymon Zinkowicz
        Ponglish Version
"""
import collada as cl
import numpy as np


def filterByMaterial(
    scene,
    materialName: str = "Material.001",
    return_blanks: bool = False,
    verbose: bool = False,
) -> list:
    """A function that returns a list of collada.geometry.BoundGeometry objects. Checks the first node of given obj.primitives() for material. Possbile to use obj.original on obj from list to rerutn not-bound geometry.
        'cl' as if collada imported as 'cl'.
        The geometry.name must adhere to naming convention name_{threeincrementalDigits} e.g. cube_033, otherwise prepareColadaObj() will throw an error.
        yellow_material = 'Material.001' ;
        blueMaterial = 'Material.002'   ;
    Args:
        scene (cl.collada.scene, <class 'collada.scene.Scene'>): A cl.Collada object. (e.g. read from file)
        materialName (str, optional): Name of the material that cointains the required color/attribute. In case of not specifing correct string for the material name - it returns every material that is not 'Material.001'". Defaults to "Material.001".
        return_blanks (bool, optional): If True then returns list with notbound geometry without materials (material as Nonetype). Defaults to False.

    Returns:
        list: List of collada.geometry.BoundGeometry objects with selected material
    """

    if type(scene) != cl.scene.Scene:
        print("Incorrect type as scene!")
        raise ValueError

    list_of_scene_geonodes = list(scene.objects("geometry"))
    if verbose == True:
        print(
            f"FUNC filterByMaterial: Amount of nodes to search though_> {len(list_of_scene_geonodes)}"
        )
    yellow_material:str = "Material.001"
    # Not used to bring more functionality as default "garbage collector"
    blueMaterial:str = "Material.002"

    list_of_yellows: list = []
    list_of_blues: list = []
    list_of_none: list = []

    for idx, obj in enumerate(list_of_scene_geonodes):
        geo = list(obj.primitives())
        triangle = geo[0]
        if triangle.material is None:
            list_of_none.append(obj)
            continue

        if verbose == True:
            print(triangle.material.name)
        if triangle.material.name == yellow_material:
            list_of_yellows.append(obj)
        else:
            list_of_blues.append(obj)

    if return_blanks == True:
        if verbose == True:
            print(f"Returned list_of_none {len(list_of_none)} objects")
        return list_of_none
    elif materialName == yellow_material:
        if verbose == True:
            print(f"Returned list_of_yellows {len(list_of_yellows)} objects")
        return list_of_yellows
    else:
        if verbose == True:
            print(f"Returned list_of_blues {len(list_of_blues)} objects")
        return list_of_blues


def filter_by_uniform_area(
    scene,
    upper_bound: float,
    lower_bound: float = 0,
    inside: bool = True,
    verbose: bool = False,
) -> list:
    """A function that returns a list of collada.geometry.BoundGeometry objects. Checks the first node of given obj.primitives() for position of ANY verticies in given area. Possbile to use obj.original on obj from list to rerutn not-bound geometry.
        'cl' as if collada imported as 'cl'.
        The geometry.name must adhere to naming convention name_{threeincrementalDigits} e.g. cube_033, otherwise prepareColadaObj() will throw an error.

    Args:
        scene (collada.scene.Scene): (cl)collada scene type object.
        upper_bound (float): Lower value for x,y,z veritcies to be checked.
        lower_bound (float, optional): Upper value for x,y,z veritcies to be checked. Defaults to 0.
        inside (bool, optional): If True then returns objects inside area specified by {upper_bound} and {lower_bound} otherwise returns objects outside of the area. Defaults to True.
        verbose (bool, optional): Prints additional information. Defaults to False.

    Returns:
        list: List of collada.geometry.BoundGeometry objects within specified boundires.
    """

    list_of_in_area: list = []
    list_of_out_of_bounds: list = []
    list_of_source_geonodes = list(scene.objects("geometry"))

    for idx_1, obj in enumerate(list_of_source_geonodes):
        geo = list(obj.primitives())
        triangle = geo[0]

        for idx_2, array_of_verts in enumerate(triangle.vertex):
            vert_in_area = np.all(
                (lower_bound < array_of_verts) & (array_of_verts < upper_bound)
            )
            if vert_in_area == True:
                list_of_in_area.append(obj)
                break
            if idx_2 == len(triangle.vertex) - 1:
                list_of_out_of_bounds.append(obj)
        if verbose == True:
            print(f"This is the amount of in_area {len(list_of_in_area)}")
            print(
                f"This is the amount of out_of_bounds {len(list_of_out_of_bounds)}"
            )
    if inside == True:
        return list_of_in_area
    else:
        return list_of_out_of_bounds


def prepare_collada_obj(
    new_scene_object: cl.scene.Scene,
    object_to_copy_from: cl.scene.Scene,
    list_to_pick_from: list,
    name_of_the_scene: str = "myscene",
    verbose: bool = False,
):
    """Function that copies specific nodes(Material, Effects, Geometry) from one scene {object_to_copy_from} to another {new_scene_object}. Works "in place" and returns the same object for code clarity.

    Args:
        new_scene_object (collada.scene.Scene): A scene object to be copied to.
        object_to_copy_from (collada.scene.Scene): A scene object to be copied from.
        list_to_pick_from (list): List of filtered collada.geometry.BoundGeometry objects.
        name_of_the_scene (str, optional): Name of the scene in new object. Defaults to "myscene".
        verbose (bool, optional): Prints additional information. Defaults to False.

    Returns:
        collada.scene.Scene: new_scene_object
    """

    amountOfObjects = len(list(object_to_copy_from.scene.objects("geometry")))
    for x_Eff in object_to_copy_from.effects:
        new_scene_object.effects.append(x_Eff)

    for x_Mat in object_to_copy_from.materials:
        new_scene_object.materials.append(x_Mat)

    index_of_correct_nodes = []
    for x_Geo in list_to_pick_from:
        x_Geo = x_Geo.original
        if verbose == True:
            print("x_Geo", x_Geo.name)
        try:
            index_of_correct_nodes.append(amountOfObjects - int(x_Geo.name[-3:]))
        except Exception as errorCode:
            print(errorCode)
            print(
                "Error while converting the name to id. Check the naming conditions (e.g. cube_001 , three numbers from the end)."
            )
            exit(1)
        new_scene_object.geometries.append(x_Geo)
    compressed_nodes = [
        val
        for idx, val in enumerate(object_to_copy_from.scene.nodes)
        if idx in index_of_correct_nodes
    ]
    try:
        print(f"Checking the first element _\n> {compressed_nodes[0].id}")
    except IndexError:
        print(
            "prepare_collada_obj : Zero nodes in the selection, check the naming conditions and filtering conditions."
        )
        exit(1)

    myscene = cl.scene.Scene(name_of_the_scene, compressed_nodes)
    new_scene_object.scenes.append(myscene)
    new_scene_object.scene = myscene

    return new_scene_object


def mean_of_centre(list_to_pick_from: list, verbose: bool = False) -> np.ndarray:
    """Function that calculates mean centre of vertices of all objects from given list.

    Args:
        list_to_pick_from (list): List of filtered collada.geometry.BoundGeometry objects.
        verbose (bool, optional): Prints additional information. Defaults to True.

    Returns:
        np.ndarray: Numpy array with x,y,c coordinates.
    """

    central_point: np.array = 0
    tmp_sum = 0
    amount: int = 0
    for x_Geo in list_to_pick_from:
        geo = list(x_Geo.primitives())
        triangle = geo[0]

        for idx_2, array_of_verts in enumerate(triangle.vertex):
            tmp_sum += array_of_verts
            amount += 1
    if amount < 1:
        print(
            "mean_of_centre : Zero nodes (verts) in the selection, check the naming conditions and filtering conditions."
        )
        exit(1)
    central_point = tmp_sum / amount

    if verbose == True:
        print("Sum of the verts:\n\t", tmp_sum)
        print("Amount of the verts:\n\t", amount)
        print("Central mean of vertices:\n\t", central_point)

    return central_point


def apply_transformation(
    scene: cl.scene.Scene,
    pivot_of_rotation=[0, 0, 0],
    transform_offsetX: float = 0,
    transform_offsetY: float = 0,
    transform_offsetZ: float = 0,
    scalevalueX: float = 1,
    scalevalueY: float = 1,
    scalevalueZ: float = 1,
    degrees_to_rotate: float = 0,
    verbose: bool = False,
) -> None:
    """Function that applies transformation to all of the objects in given scene

    Args:
        scene (cl.scene.Scene): (cl)collada scene type object.
        pivot_of_rotation (list, optional): Coordinates of axis [X,Y,Z] to rotate. Values diffrent than 1 also scale. Defaults to [0, 0, 0].
        transform_offsetX (float, optional): Transformation albon X axis. Defaults to 0.
        transform_offsetY (float, optional): Transformation albon Y axis. Defaults to 0.
        transform_offsetZ (float, optional): Transformation albon Z axis. Defaults to 0.
        scalevalueX (float, optional): Scaling along X axis. Defaults to 1.
        scalevalueY (float, optional): Scaling along Y axis. Defaults to 1.
        scalevalueZ (float, optional): Scaling along Z axis. Defaults to 1.
        degrees_to_rotate (float, optional): Amount of degrees to rotate (These are being converted into radians). Defaults to 0.
        verbose (bool, optional): Prints additional information. Defaults to False.
    """
    matrixScale = cl.scene.ScaleTransform(
        scalevalueX, scalevalueY, scalevalueZ
    )
    cos = np.cos(np.radians(degrees_to_rotate))
    sin = np.sin(np.radians(degrees_to_rotate))
    x, y, z = pivot_of_rotation[0], pivot_of_rotation[1], pivot_of_rotation[2]
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
    return scene


def zeroed_coords(
    scene: cl.scene.Scene,
    old_inverted_matrix: np.ndarray = np.identity(4),
    verbose: bool = False,
) -> list:
    """Function that zeroes the transformation matrix of all objects in node and returns list of inverted matricies of them. To be used with reverse_translation() and reverse_rotation().
    {old_inverted_matrix} is optional, but a diffrent matrix passed can produce diffrent results and "return" return the geometry to a diffrent place.
    Example:
        # Global coordinates == local coordinates
        negativeTranslateList = zeroed_coords(scene= newSceneMesh.scene)
        # Bringing back old rotation
        reverse_rotation(scene= newSceneMesh.scene, old_inverted_matrix= negativeTranslateList)
        # Bringing back old translation
        reverse_translation(scene= newSceneMesh.scene, old_inverted_matrix= negativeTranslateList)
        # And the geometry is back in the same place

    Args:
        scene (cl.scene.Scene): (cl)collada scene type object.
        old_inverted_matrix (np.ndarray, optional): Inverted matrix of previous transforms. Defaults to np.identity(4).
        verbose (bool, optional): Prints additional information. Defaults to False.

    Returns:
        list: list of inverted matricies.
    """
    listOf_minusTranslates = []
    for idx, nodeX in enumerate(scene.nodes):
        transforms_old = nodeX.transforms[0]
        transforms_old_INV = np.linalg.inv(transforms_old.matrix)

        if verbose == True:
            print(f"Old_matrix _>\n {transforms_old.matrix}")

        final_matrix = cl.scene.MatrixTransform(old_inverted_matrix.flatten())
        listOf_minusTranslates.append(transforms_old_INV)
        scene.nodes[idx].transforms[0] = final_matrix
        (scene.nodes[idx]).save()
        if verbose == True:
            print(f"final_matrix _>\n {final_matrix.matrix}")
    return listOf_minusTranslates


def reverse_translation(
    scene: cl.scene.Scene,
    old_inverted_matrix=np.identity(4),
    verbose: bool = False,
):
    """Function that brings back x,y,z translation coordinates before {zeroed_coords()}

    Args:
        scene (cl.scene.Scene): (cl)collada scene type object.
        old_inverted_matrix (np.ndarray, optional): Inverted matrix of previous transforms. Defaults to np.identity(4).
        verbose (bool, optional): Prints additional information. Defaults to False.
    """
    for idx, nodeX in enumerate(scene.nodes):
        transforms_curernt = nodeX.transforms[0]
        transforms_old_INV = np.linalg.inv(old_inverted_matrix[idx])
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


def reverse_rotation(
    scene: cl.scene.Scene,
    old_inverted_matrix: np.ndarray = np.identity(4),
    verbose: bool = False,
):
    """Function that brings back x,y,z rotation coordinates before {zeroed_coords()}

    Args:
        scene (cl.scene.Scene): (cl)collada scene type object.
        old_inverted_matrix (np.ndarray, optional): Inverted matrix of previous transforms. Defaults to np.identity(4).
        verbose (bool, optional): Prints additional information. Defaults to False.
    """

    for idx, nodeX in enumerate(scene.nodes):
        transforms_curernt = nodeX.transforms[0]
        transforms_old_INV = np.linalg.inv(old_inverted_matrix[idx])
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
