# Times Table Modulo

Inspired by [Mathologer's video] (https://youtu.be/qhbuKbxJsk8), this is a Python OpenGL implementation of modular arithmetic times tables. 

## Installation
Python 3 is required for this project. This project uses pipenv to manage libraries. Run `pipenv sync` then `pipenv run python3 ttmodulo.py` to run the program. This project uses the following libraries:
* numpy: For math backend
* pyrr: For matrix backend
* moderngl: For OpenGL backend
* modengl-window[tk]: For TK windowing

All OpenGL shaders are hardcoded into the `ttmodulo.py` file. 

## Variables in ttmodulo.py

If you wish to modify the simulation parameters, you may edit the constants at the top of the `ttmodulo.py` file:

Variables | Type | Explanation
--------- | ----- | -----------
`VERTEX_COUNT` | int | The number of vertices defining the outer circle. Must have at least 2
`MULTIPLIER` | float | The initial table multiplier
`MULTIPLIER_DERIV` | float | How much to change the multiplier every second. The multiplier is automatically bounded by 0 and `VERTEX_COUNT`
`CIRCLE_RADIUS` | float | Percentage of the dimensions the radius stretches (1.0 = whole window)
`HSV` | float | The initial hue of the model's HSV color
`HSV_DERIV` | float | How much to change the hue every second. The hue is automatically bounded by 0 and 1
`SATURATION` | float | The saturation value of the model's HSV color
`VALUE` | float | The value value of the model's HSV color
`WINDOW_DIMS` | (int,int) | Tuple of the window dimensions. Square recommended

## Math explanation
