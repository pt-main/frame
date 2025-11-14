import builtins
import numpy as np
cimport numpy as cnp

ctypedef long long int i64

ctypedef fused scalar_number:
    i64_t
    double
    int
    float

ctypedef scalar_number snum

ctypedef fused array_element:
    int
    float
    double

ctypedef struct Point2d:
    double x
    double y

ctypedef struct Point3d:
    double x
    double y
    double z

cdef class Vector2d:
    cdef Point2d[::1] points_array 
    cdef int size
    
    def __init__(self, points):
        self.size = len(points)
        self.points_array = np.array(points, dtype=[('x', 'f8'), ('y', 'f8')])
    
    def __getitem__(self, int index):
        return (self.points_array[index].x, self.points_array[index].y)

def process_scalar(snum x) -> snum:
    cdef snum result = x * 2
    return result

def process_array(array_element[::1] arr) -> array_element:
    cdef int i
    cdef array_element total = 0
    
    for i in range(arr.shape[0]):
        total += arr[i]
    
    return total

def create_point2d(double x, double y) -> Point2d:
    cdef Point2d p
    p.x = x
    p.y = y
    return p

def distance2d(Point2d a, Point2d b) -> double:
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5