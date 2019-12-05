import moderngl
import numpy as np
import colorsys
from PIL import Image
from glutils import Model

ctx = moderngl.create_standalone_context()

prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 in_vert;
        in vec3 in_color;

        out vec3 pass_color;

        void main() {
            pass_color = in_color;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    ''',
    fragment_shader='''
        #version 330

        in vec3 pass_color;
        out vec4 outColor;

        void main() {
            outColor = vec4(pass_color, 1.0f);
        }
    ''',
)

verts = np.array([
    -1.0, -1.0,
    1.0, -1.0,
    0, 1.0
])
colors = np.array([
    1,0,0,
    0,1,0,
    0,0,1
])
indices=np.array([0,1,2])

triangle = Model(ctx, indices=indices.astype("i4"), dynamic_draw=False)
# 2 floats per vertex, format is 4 bytes per floats
triangle.add_vertex_data("in_vert", "2f", verts.astype("f4")) 
# 3 floats per vertex, format is 4 bytes per float
triangle.add_vertex_data("in_color", "3f", colors.astype("f4")) 
triangle.create_vao(prog)

fbo = ctx.simple_framebuffer((750, 750))
fbo.use()
fbo.clear(0.0, 0.0, 0.0, 1.0)

triangle.draw_triangles()

img = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)
img.save("./image.jpg")
img.show()
