import numpy
import math
from pyrr import Matrix44, Vector3

# Credit to https://www.lfd.uci.edu/~gohlke/code/transformations.py.html

class PositionMatrix:
    """Represents a 4x4 matrix managing translation, position, and scale"""

    def __init__(self, position, pitch, yaw, roll, scale):
        self.position = Vector3(position)
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.scale = scale

    def simulate_move_xz(self, yaw_delta, distance):
        """Performs a translation of length distance in the direction of yaw in the xy plane"""
        # Negate yaw to negate viewport matrix. It just works idk
        turn = -self.yaw + yaw_delta
        dx = distance * cos(math.radians(turn))
        dz = distance * cos(math.radians(turn))
        return Vector3(dx, 0, dz)

    def set_matrix(self, m):
        self.m = m

    def build_matrix(self):
        m = Matrix44.identity()
        m = Matrix44.from_x_rotation(math.radians(self.pitch)) * m
        m = Matrix44.from_y_rotation(math.radians(self.yaw)) * m
        m = Matrix44.from_z_rotation(math.radians(self.roll)) * m
        m = Matrix44.from_translation(self.position) * m
        self.m = m

    def get_matrix(self):
        self.build_matrix()
        return numpy.array(self.m)

class ViewportMatrix(PositionMatrix):
    """Manages a 4x4 matrix managing a camera""" 

    def __init__(self, position, pitch, yaw, roll, width, height, fov, near_plane, far_plane, tp, tp_distance):
        PositionMatrix.__init__(self, position, pitch, yaw, roll, 1)
        self.width = width
        self.height = height
        self.near_plane = near_plane
        self.far_plane = far_plane
        self.fov = fov
        self.tp = tp
        self.tp_distance = tp_distance

    def build_proj_matrix(self):
        self.p = Matrix44.perspective_projection(self.fov, 
                self.width / self.height, self.near_plane, self.far_plane)

    def build_matrix(self):
        # Note that by nature, a camera perspective inverts everything
        # So we negate everything and also do it in reverse

        # Overrides PositionMatrix 
        m = Matrix44.identity()
        m = Matrix44.from_translation(-1 * self.position) * m
        m = Matrix44.from_z_rotation(-math.radians(self.roll)) * m
        m = Matrix44.from_y_rotation(-math.radians(self.yaw)) * m
        m = Matrix44.from_x_rotation(-math.radians(self.pitch)) * m
        if self.tp:
            # Third person enabled
            m = Matrix44.from_translation([0,0,-self.tp_distance]) * m
        

        self.m = m

    def get_matrix(self):
        self.build_matrix()
        self.build_proj_matrix()
        return numpy.array(self.p * self.m)
