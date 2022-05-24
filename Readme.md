# Filtering script

## Usage

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

## Contributing

Zapraszam na githuba <:
<https://github.com/Siponek/colladaPythonWrapper.git>
