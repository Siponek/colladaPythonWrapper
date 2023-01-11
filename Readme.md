# Filtering script

## Usage

Run the Filter.py. To change the results pick a diffrent fucntion in script.

```python
        # ? Chaning the listToPickFrom to quickly test out the fucntions

        listToPickFrom = filterByMaterial(scene=mesh.scene, verbose=False)

        listToPickFrom = filterByMaterial(
            scene=mesh.scene, materialName="Material.002"
        )

        listToPickFrom = filterByUniformArea(scene=mesh.scene, upper_bound=15)
```

### Examples

```python

# ! The working combination for a rotation around its own axis
negativeTranslateList = zeroedCoords(scene= newSceneMesh.scene)
reverseRotation(scene= newSceneMesh.scene, oldInvertedMatrix= negativeTranslateList)
applyTransformation(scene= newSceneMesh.scene, pivotOfRotation = [0,0,1], degreesToRotate=20, localTransform = False)
reverseTranslation(scene= newSceneMesh.scene, oldInvertedMatrix= negativeTranslateList)
applyTransformation(scene= newSceneMesh.scene, transform_offsetY= 20,scalevalueX = 1, scalevalueY = 1, scalevalueZ = 1, verbose= False)
```

```python
# ! The working combination for a rotation around axis of whole set
applyTransformation(scene= newSceneMesh.scene, transform_offsetX= originPoint_negative[0],transform_offsetY= originPoint_negative[1],transform_offsetZ= originPoint_negative[2] ,scalevalueX = 1, scalevalueY = 1, scalevalueZ = 1, verbose= False)

applyTransformation(scene= newSceneMesh.scene, pivotOfRotation = [0,0,1], degreesToRotate=30, localTransform = False)

applyTransformation(scene= newSceneMesh.scene, transform_offsetX= originPoint[0],transform_offsetY= originPoint[1],transform_offsetZ= originPoint[2] ,scalevalueX = 1, scalevalueY = 1, scalevalueZ = 1, verbose= False)
applyTransformation(scene= newSceneMesh.scene, transform_offsetY= 20,scalevalueX = 1, scalevalueY = 1, scalevalueZ = 1, verbose= False)

```
## TODO

<!-- .gitignore <br /> -->
requirements.txt <br />
<!-- fix snake-case and camel case <br /> -->
Add argprase for more generic approach when using script via CLI <br />
Add method chaning

## Contributing
Feel free to contribute to this project. :><br />
