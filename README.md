# Times Table Modulo

Inspired by [Mathologer's video](https://youtu.be/qhbuKbxJsk8), this is a Python OpenGL implementation of modular multiplication tables, featuring multiplier and color changing over time.

## Sample renders
VERTEX_COUNT=1000 MULTIPLIER=4.0
![image](https://i.imgur.com/9trkvJ2.png)

VERTEX_COUNT=1000 MULTIPLIER=345.0
![image](https://i.imgur.com/vuVGYfG.png)

## Installation
Python 3, pip, and pipenv are required for this project. Run `pipenv install` to install required libraries under pipenv, then execute `pipenv run python3 ttmodulo.py` to run the program. All OpenGL shaders are hardcoded into the `ttmodulo.py` file and do not need to be externally provided. 

## Quick math explanation

The two impotant variables are `VERTEX_COUNT` and `MULTIPLIER`. A set of `VERTEX_COUNT` points are evenly spaced around a circle and indexed from 0 to `VERTEX_COUNT - 1`. Then for every point, a corresponding point is calculated with index equal to `(point's index) * MULTIPLIER % VERTEX_COUNT`. A line is drawn between the two points. The modulo operation ensures that multiplying will always map to an existing point. Animations are rendered by changing `MULTIPLIER` over time. If the multiplier is a float, the index is the floor of the result after the modulo is taken.

## Project Details

### Simulation parameters

If you wish to modify the simulation parameters, you may edit the constants at the top of the `ttmodulo.py` file:

Variable | Type | Explanation
--------- | ----- | -----------
`VERTEX_COUNT` | int | The number of vertices defining the outer circle. Must have at least 2
`MULTIPLIER` | float | The initial table multiplier
`MULTIPLIER_DERIV` | float | How much to change the multiplier every second. The multiplier is automatically bounded by 0 and `VERTEX_COUNT`
`CIRCLE_RADIUS` | float | Percentage of the dimensions the radius stretches (1.0 = whole window)
`HSV` | float | The initial hue of the model's HSV color
`HSV_DERIV` | float | How much to change the hue every second. The hue is automatically bounded by 0 and 1
`SATURATION` | float | The saturation value of the model's HSV color
`VALUE` | float | The value value of the model's HSV color
`WINDOW_DIMS` | (int,int) | Tuple of the window dimensions. 1:1 aspect ratio recommended

### Libraries used

This project uses the following libraries:
* numpy: For math backend
* pyrr: For matrix backend
* moderngl: For OpenGL backend
* modengl-window[tk]: For TK windowing

### Files

* `ttmodulo.py`: The main program
* `glutils.py`: Utilities to interface with OpenGL 
* `mathutils.py`: Classes facilitating math operations
* `Pipfile`, `Pipfile.lock`: For pipenv
* `old/`: Miscellaneous programs unrelated to the project