"""
A collection of utilities to manage OpenGL and ultimately
abstract the hardware calls from the program
"""

import moderngl as gl


def enable_depth_test(ctx):
    """Enables the depth test flag"""
    ctx.enable(gl.DEPTH_TEST)

def enable_cull_face(ctx):
    """Enables the cull face flag"""
    ctx.enable(gl.CULL_FACE)

def disable_depth_test(ctx):
    """Disables the depth test flag"""
    ctx.disable(gl.DEPTH_TEST)

def disable_cull_face(ctx):
    """Disables the cull face flag"""
    ctx.disable(gl.DEPTH_TEST)


class Model:
    """Manages a VAO of VBOs for rendering
    Assumes that data handed to it are numpy arrays"""
    
    def set_indices(self, indices):
        """Used to dynamicly change indices"""
        self.indices_vbo.write(indices.tobytes())

    def __init__(self, ctx, indices=[], dynamic_draw=False):
        """Initiates a model
        indices are optional but may be provided upon creation
        indices are assumed to contain 4-byte ints
        dynamic_draw determines whether indices should be
            buffered dynamically or not"""
        self.ctx = ctx
        self.vbos = list()

        if len(indices) > 0:
            if dynamic_draw:
                self.indices_vbo = self.ctx.buffer(data=None, reserve=4*len(indices), dynamic=True)
                self.set_indices(indices)
            else:
                self.indices_vbo = self.ctx.buffer(indices.tobytes())


    def add_vertex_data(self, location, data_type, data):
        """Creates a VBO and stores the vertex pointers
        data is assumed to be 4-byte floats
        This is the GL equivalent to vertex attrib pointers"""
        vbo = self.ctx.buffer(data.tobytes())
        self.vbos.append( (vbo, data_type, location) )
        
    def create_vao(self, program):
        """Creates the VAO for the model
        Vertex data should be given before this is called"""
        self.vao = self.ctx.vertex_array(program, self.vbos, 
                index_buffer=self.indices_vbo)

    def draw_lines(self):
        """Draw lines"""
        self.vao.render(gl.LINES)
        
    def draw_triangles(self):
        """Draw triangles"""
        self.vao.render(gl.TRIANGLES)
