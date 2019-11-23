import moderngl as gl

class Model:
    """Manages a VAO of VBOs for rendering

    Assumes that data handed to it are numpy arrays"""
    
    def set_indices(self, indices):
        """Used to dynamicly change indices"""
        self.indices_vbo.write(arr.tobytes())

    def __init__(self, ctx, indices=[], dynamic_draw=False):
        self.ctx = ctx
        self.vbos = list()

        if len(indices) > 0:
            if dynamic_draw:
                self.indices_vbo = self.ctx.buffer(data=None, dynamic=True)
                self.set_indices(indices)
            else:
                self.indices_vbo = self.ctx.buffer(indices.tobytes())


    def add_vertex_data(self, location, data_type, data):
        vbo = self.ctx.buffer(data.tobytes())
        self.vbos.append( (vbo, data_type, location) )
        
    def create_vao(self, program):
        self.vao = self.ctx.vertex_array(program, self.vbos, 
                index_buffer=self.indices_vbo)

    def draw(self, shape):
        self.vao.render(shape)

    def draw_lines(self):
        self.draw(gl.LINES)
        
    def draw_triangles(self):
        self.draw(gl.TRIANGLES)
