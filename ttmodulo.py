"""
Andy Nguyen, 11/22/19
Implements the MVP matrix with some basic cubes
"""

import moderngl_window as mglw
from moderngl_window.conf import settings
from glutils import Model
from mathutils import SpeedRegulator
import numpy as np
import colorsys
import math

class MyWindow:

    def __init__(self, gl_version, size, fullscreen, resizable, title, cursor):
        config = {
            #"class": "moderngl_window.context.tk.Window",
            "gl_version": gl_version,
            "size": size,
            "aspect_ratio": size[1]/size[0],
            "fullscreen": fullscreen,
            "resizable": resizable,
            "title": title,
            "vsync": False,
            "cursor": cursor,
            "samples": 0
        }
        settings.WINDOW = dict(list(settings.WINDOW.items()) + list(config.items()))
        self.window = mglw.create_window_from_settings()
        self.ctx = self.window.ctx

    def swap_buffers(self):
        self.window.swap_buffers()

    def clear(self):
        self.window.clear()

    def should_close(self):
        return self.window.is_closing

    def destroy(self):
        pass

# Create window and shaders
window = MyWindow((3,3), (750, 750), False, True, "TTModulo", True)
ctx = mglw.ctx()
prog = ctx.program(
    vertex_shader="""
    #version 330
    in vec2 position;
    void main() {
        gl_Position = vec4(-position.x, position.y, 0.0f, 1.0f);
    }
    """,
    fragment_shader="""
    #version 330
    //precision mediump float;
    uniform vec3 color;
    out vec4 outColor;
    void main() {
        outColor = vec4(color, 1.0f);
    }
    """
)

def gen_vertices(vertex_count, circle_radius):
    vertex_array = list()
            
    for i in range(vertex_count):
        angle = 2.0 * math.pi / VERTEX_COUNT * i
        vertex_array.append( circle_radius * math.cos(angle) )
        vertex_array.append( circle_radius * math.sin(angle) )

    return np.array(vertex_array, dtype=np.float32)

def gen_indices(vertex_count, multiplier):
    indices_array = list()

    for i in range(vertex_count):
        indices_array.append(i)
        indices_array.append(int( (i * multiplier) % vertex_count))
                                                            
    return np.array(indices_array, dtype=np.int32)

# Model constants
VERTEX_COUNT = 500
MULTIPLIER = 4.0
MULTIPLIER_DERIV = 1.0
CIRCLE_RADIUS = 1.0
HSV = 0.0
HSV_DERIV = 0.125
SATURATION = 1.0
VALUE = 1.0

# Generate model
vertex_array = gen_vertices(VERTEX_COUNT, CIRCLE_RADIUS)
indices_array = gen_indices(VERTEX_COUNT, MULTIPLIER)
circle_model = Model(ctx, indices=indices_array.astype("i4"), dynamic_draw=False)
# 2 floats per vertex, format is 4 bytes per floats
circle_model.add_vertex_data("position", "2f", vertex_array.astype("f4")) 
circle_model.create_vao(prog)

# Prep for rendering
speedreg = SpeedRegulator(1)
last_fps = 0

while not window.should_close():
    # Begin calculations
    speed = speedreg.get_next_delta()

    # Update indices
    MULTIPLIER += MULTIPLIER_DERIV * speed
    indices_array = gen_indices(VERTEX_COUNT, MULTIPLIER)
    circle_model.set_indices(indices_array)

    # Update color
    HSV += HSV_DERIV * speed
    HSV %= 1
    curr_color = colorsys.hsv_to_rgb(HSV, SATURATION, VALUE)

    # Prep rendering
    window.clear()
    ctx.clear()
    prog["color"].write(np.array(curr_color).astype("f4").tobytes())

    # Draw model
    circle_model.draw_lines()

    # End rendering
    window.swap_buffers()
    if speedreg.fps != last_fps:
        print("FPS: ", speedreg.fps)
        last_fps = speedreg.fps
