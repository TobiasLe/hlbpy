# hlbpy

hlbpy (high level blender python) is a library intended to make it more convinient to set up scenes in Blender with python. 

If you have ever used the blender python api, you have probably noticed that it is not really designed to quickly build scenes with it. Even doing simple stuff (e.g. adding a cube to the scene) can easily require several lines of code. hlbpy esentially adds a high level layer above the blender python api to make typical scene building tasks easier. 

I mainly write this library for my myself, to make it easier to create videos for my YouTube channel: [youtube.com/c/marblescience](https://www.youtube.com/c/marblescience)
Anyway, you are welcome to use the code! Just be aware that it is far from complete, far from well tested, and far from well documented.

## Usage

Here is some example code to give you an idea how you can use hlbpy.

```python
import hlbpy
from math import pi
import numpy as np

hlbpy.run_in_blender()

scene = hlbpy.Scene.from_context()

cubes = scene.link(hlbpy.Collection("Cubes"))

big_cube = cubes.link(hlbpy.mesh.Cube(edge_length=2, name="BigCube"))
small_cube = cubes.link(hlbpy.mesh.Cube(edge_length=1, name="SmallCube"))

small_cube.location = (0, 0, 2.5)

small_cube.parent = big_cube

big_cube.set_keyframes("location", np.sin(np.linspace(0, 2*pi, 60)), index=2)
small_cube.set_keyframes("rotation_euler", [[0, 0, 0], [0, 0, 2*pi]], frame_numbers=[0, 60])

scene.frame_end = 60
```
In this example, we create a new collection "Cubes".  
We link two cubes to this collection.  
We change the location of one cube.  
We parent one cube to the other.  
Finally, we add keyframes to animate the cubes.  

Once executed, this code opens blender, and this is what you would see:

<img src="images/basic_scene.gif"/>
