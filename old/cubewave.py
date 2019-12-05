"""
Andy Nguyen, 11/22/19
Implements the MVP matrix with some basic cubes
"""

import math
import colorsys
import numpy as np
import moderngl_window as mglw
from moderngl_window.conf import settings
import glutils
from glutils import Model
from mathutils import PositionMatrix, ViewportMatrix, SpeedRegulator
import colorsys

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
        mglw.conf.settings.WINDOW = dict(list(settings.WINDOW.items()) + list(config.items()))
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

# Initiate OpenGL, create window and program
window = MyWindow((3,3), (1000, 1000), False, True, "Cube Window", True)
ctx = mglw.ctx()
glutils.enable_depth_test(ctx)
glutils.enable_cull_face(ctx)
prog = ctx.program(
    vertex_shader="""
        #version 330
        in vec3 position;
        
        uniform vec3 color;
        uniform mat4 u_mm;
        uniform mat4 u_vpc;
        
        out vec4 pass_color;

        vec3 hsv2rgb(vec3 c) {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }

        void main() {
            gl_Position = u_vpc * u_mm * vec4(position.x, position.y, position.z, 1.0f);
            pass_color = vec4(color, 1.0f);
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
cube.create_vao(prog)

# Terrain parameters
GRIDSIZE = (6,6)
SCALE = 1

# Generate cubes
cubes = list()
x = GRIDSIZE[0] / -2
while x <= GRIDSIZE[0] / 2:
    cube_row = list()
    z = GRIDSIZE[1] / -2
    while z <= GRIDSIZE[1] / 2:
        # Divide scale by two because our cube is defined by -1 to 1 coords
        y = math.sin(x*x + z*z)
        cube_row.append( [PositionMatrix([x,y,z], 0, 0, 0, SCALE/2), [0,0,0]] )
        z += SCALE
    cubes.append(cube_row)
    x += SCALE
# Prep for rendering
vpc = ViewportMatrix([0,0, 0],25,0,0,1200,1200,90,0.1,25,True,8)
speedreg = SpeedRegulator(1)
last_fps = 0
time = 0

while not window.should_close():

    # Begin calculations
    speed = speedreg.get_next_delta()
    time += speed

    # Update camera rotation
    vpc.yaw = (vpc.yaw + 45 * speed) % 360
    vpc.build_view_matrix()

    # Update cubes' z coord
    for r in cubes:
        for c in r:
            # Generate position
            p = c[0].position
            dist = p[0] * p[0] + p[2] * p[2] + time
            p[1] = math.sin(dist)#((-1) ** (int(dist+1) % 2) * dist) % 2 * SCALE
            c[0].position = p
            c[0].build_matrix()

            # Generate color
            c[1] = np.array(colorsys.hsv_to_rgb((p[1]+1)/3, 1, 1)).astype("f4") 

    # Prep rendering
    window.clear()
    prog["u_vpc"].write(vpc.get_matrix())

    # Draw cubes
    for r in cubes:
        for c in r:
            prog["color"].write(c[1])
            prog["u_mm"].write(c[0].get_matrix())
            cube.draw_triangles()

    # End rendering
    window.swap_buffers()
    if speedreg.fps != last_fps:
        print("FPS: ", speedreg.fps)
        last_fps = speedreg.fps

