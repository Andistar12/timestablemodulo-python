"""
Andy Nguyen, 11/22/19
Implements the MVP matrix with some basic cubes
"""

import moderngl as gl
import moderngl_window as mglw
from moderngl_window.conf import settings
from glutils import Model, SpeedRegulator
from mathutils import PositionMatrix, ViewportMatrix
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
window = MyWindow((3,3), (750, 750), False, True, "Cube Window", True)
ctx = mglw.ctx()
prog = ctx.program(
    vertex_shader="""
        #version 330
        in vec3 position;
        in vec3 color;
        uniform mat4 u_mm;
        uniform mat4 u_vpc;
        out vec4 pass_color;
        void main() {
            gl_Position = u_vpc * u_mm * vec4(position.x, position.y, position.z, 1.0f);
            pass_color = vec4(color, 1.0);
        }
    """,
    fragment_shader="""
    #version 330
    //precision mediump float;
    in vec4 pass_color;
    out vec4 outColor;
    void main() {
        outColor = pass_color;
    }
    """
)

# Model data
cube_verts = np.array([
                # ZYX
    1,1,1,      # FTL
    -1,1,1,     # FTR
    -1,1,-1,    # BTR
    1,1,-1,     # BTL
    1,-1,1,     # FBR
    -1,-1,1,    # FBL
    -1,-1,-1,   # BBL
    1,-1,-1     # BBR
], dtype=np.float32)
cube_colors = np.array([
    1,1,1,
    1,0,0,
    0,0,1,
    0,1,0,
    1,1,0,
    1,0,1,
    0,1,1,
    0.5,0.5,0.5
], dtype=np.float32)
cube_indices = np.array([
    0,2,1,0,3,2,    # Top
    0,5,4,0,1,5,    # Front
    0,7,3,0,4,7,    # Right
    2,5,1,2,6,5,    # Left
    3,6,2,3,7,6,    # Back
    6,4,5,6,7,4     # Bottom
], dtype=np.int32)

# Generate model
cube = Model(ctx, indices=cube_indices.astype("i4"), dynamic_draw=False)
cube.add_vertex_data("position", "3f", cube_verts.astype("f4"))
cube.add_vertex_data("color", "3f", cube_colors.astype("f4"))
cube.create_vao(prog)

# Matrices
model_pos = PositionMatrix([0,0,0], 0,0,0,1)
model2_pos = PositionMatrix([0,0,-3],0,180,0,1)
vpc = ViewportMatrix([0,0, 0],25,0,0,750,750,90,0.1,25,True,8)

# Prep for rendering
speedreg = SpeedRegulator(1)
last_fps = 0
ctx.enable_only(gl.DEPTH_TEST | gl.CULL_FACE)

while not window.should_close():

    # Begin calculations
    speed = speedreg.get_next_delta()
    vpc.yaw = (vpc.yaw + 90 * speed) % 360

    # Prep rendering
    window.clear()
    ctx.clear()
    prog["u_vpc"].write(vpc.get_matrix().astype("f4"))

    # Draw models
    prog["u_mm"].write(model_pos.get_matrix().astype("f4"))
    cube.draw_triangles()
    prog["u_mm"].write(model2_pos.get_matrix().astype("f4"))
    cube.draw_triangles()

    # End rendering
    window.swap_buffers()
    if speedreg.fps != last_fps:
        print("FPS: ", speedreg.fps)
        last_fps = speedreg.fps

