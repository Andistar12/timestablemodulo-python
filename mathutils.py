"""
A collection of math utilities to manage matrices and timing
"""

import numpy
import math
import time
from pyrr import Matrix44, Vector3


class SpeedRegulator:
    """Manages timing for a render loop, also includes an FPS counter"""
            
    def reset(self):
        """Resets the timer and FPS"""
        self.last_time = time.time()
        self.last_time_fps = time.time()
        self.fps_counter = 0
        self.fps = 0
            
    def get_next_delta(self):
        """Call this method during the render loop to scale 
        time accordingly"""
        current_time = time.time()
        speed = current_time - self.last_time
        self.last_time = current_time
        
        self.fps_counter += 1
        if (current_time - self.last_time_fps) > self.avg_time:
            self.fps = self.fps_counter / (current_time - self.last_time_fps)
            self.fps_counter = 0
            self.last_time_fps = current_time
        
        return speed
        
    def get_fps(self):
        """Returns the calculated FPS"""
        return self.fps 
        
    def __init__(self, avg_time):
        """Initiates the timer
        avg_time is how often the FPS counter should be 
            updated, in seconds"""
        self.avg_time = avg_time
        self.reset()


class PositionMatrix:
    """Represents a 4x4 float matrix managing translation, position, and scale
    Uses pyrr for computation but stores as numpy array"""

    def __init__(self, position, pitch, yaw, roll, scale):
        """Initiates a PoaitionMatrix
        Arguments:
        - position: tuple length 3, xyz location of point
        - pitch/yaw/roll: floats, rotation along xyz axes
        - scale: tuple length 3 or float, scales either each axis 
            individually or all by the given value

        Automatically builds the matrices as well
        """

        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.scale = scale

        self.build_matrix()

    def set_matrix(self, m):
        """Manually sets the internal matrix to be the given matrix"""
        self.m = m

    def build_matrix(self):
        """Builds and stores the transformation matrix internally"""

        m = Matrix44.identity()
        if isinstance(self.scale, list) or isinstance(self.scale, tuple):
            m.m11 = self.scale[0]
            m.m22 = self.scale[1]
            m.m33 = self.scale[2]
        else:
            m *= self.scale
            m.m44 = 1
        m = Matrix44.from_x_rotation(math.radians(self.pitch)) * m
        m = Matrix44.from_y_rotation(math.radians(self.yaw)) * m
        m = Matrix44.from_z_rotation(math.radians(self.roll)) * m
        m = Matrix44.from_translation(Vector3(self.position)) * m
        self.m = numpy.array(m).astype("f4")

    def get_matrix(self):
        """Returns the transformation matrix"""
        return self.m


class ViewportMatrix():
    """Manages a 4x4 float matrix managing a perspective camera 
    Uses pyrr for computation but stores as numpy array"""

    def __init__(self, position, pitch, yaw, roll, width, height, fov, near_plane, far_plane, tp, tp_distance):
        """Initiates a ViewportMatrix
        View matrix arguments:
        - position: tuple length 3, location of camrea
        - pitch/yaw/roll: floats, rotations along xyz axis

        Perspective matrix arguments:
        - width/height: ints, frame width and height
        - fov: int, field of view in y direction
        - near_plane: float, clipping for plane closest to camera (recommended=0.1)
        - far_plane: float, clipping for plane farthest from camera
        - tp: boolean, whether third person camera should be used
        - tp_distance: float, distance from camera location to actual viewport location

        Automatically builds the MVP matrix as well
        """

        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.width = width
        self.height = height
        self.near_plane = near_plane
        self.far_plane = far_plane
        self.fov = fov
        self.tp = tp
        self.tp_distance = tp_distance

        # Set p to identity so these method auto build the MVP
        self.p = Matrix44.identity()
        self.build_view_matrix()
        self.build_proj_matrix()

    def build_proj_matrix(self):
        """Builds and stores the perspective matrix internally
        Automatically builds the MVP matrix as well"""
        self.p = Matrix44.perspective_projection(self.fov, 
                self.width / self.height, self.near_plane, self.far_plane)

        self.mvp = numpy.array(self.p * self.m).astype("f4")

    def build_matrix(self):
        """Builds and stores the viewport matrix internally
        Automatically builds the MVP matrix as well"""
        # Note that by nature, a camera perspective inverts everything
        # So we negate everything and also do it in reverse

        # Overrides PositionMatrix, reverse everything, ignore scale 
        m = Matrix44.identity()
        m = Matrix44.from_translation(-1 * Vector3(self.position)) * m
        m = Matrix44.from_z_rotation(-math.radians(self.roll)) * m
        m = Matrix44.from_y_rotation(-math.radians(self.yaw)) * m
        m = Matrix44.from_x_rotation(-math.radians(self.pitch)) * m
        if self.tp:
            # Third person enabled
            m = Matrix44.from_translation([0,0,-self.tp_distance]) * m
        
        self.m = m
        self.mvp = numpy.array(self.p * self.m).astype("f4")

    def build_view_matrix(self):
        """Alias for build_matrix"""
        self.build_matrix()

    def get_matrix(self):
        """Returns the MVP matrix"""
        return self.mvp
