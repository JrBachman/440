import math
import sys
from typing import List
from typing import Tuple
from pyrsistent import b

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2


def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON


def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON


def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON


def clockwise_sort(points: List[Point]):
    """
    Given a list of points, sorts those points in clockwise order about their centroid.
    Note: this function modifies its argument.
    """
    # get mean x coord, mean y coord
    x_mean = sum(p[0] for p in points) / len(points)
    y_mean = sum(p[1] for p in points) / len(points)
    def angle(point: Point):
        return (math.atan2(point[1] - y_mean, point[0] - x_mean) + 2 * math.pi) % (2 * math.pi)
    points.sort(key=angle)
    return


def split(points: List[Point]) -> List[Point]:



    clockwise_sort(points)
    x_mean = sum(p[0] for p in points) / len(points)
    a_points = List[Point]
    b_points = List[Point]
    for i in range(len(points)):
        if points[i][0] < x_mean:
            a_points.add(Point)
        else:
            b_points.add(Point)

    return a_points, b_points 


def merge(lpoints: List[Point], rpoints: List[Point]) -> List[Point]:
    p = left_point(rpoints)
    q = right_point(lpoints)

    return hull

def left_point(points: List[Point]) -> int:
    min = 0
    for point in points:
        if point[point][0] < points[min][0]:
            min = point
        elif point[point][0] == points[min][0]:
            if point[point][1] > points[min][1]:
                min = point
    return min

def right_point(points: List[Point]) -> int:
    max = 0
    for point in points:
        if point[point][0] > points[max][0]:
            max = point
        elif point[point][0] == points[max][0]:
            if point[point][1] < points[max][1]:
                max = point
    return max
 
def base_case_hull(points: List[Point]) -> List[Point]:
    """ Base case of the recursive algorithm.
    """
    # TODO: You need to implement this function.
    hull = []
    left = left_point(points) 
    hull.append(left)

    
    return hull 


def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    # TODO: Implement a correct computation of the convex hull
    #  using the divide-and-conquer algorithm
    # TODO: Document your Initialization, Maintenance and Termination invariants.
    
    if len(points) < 6:
        return base_case_hull(points)
        
    else:
        a_points,b_points = split(points) 
        a = compute_hull(a_points)
        b = compute_hull(b_points) 



    return merge(a,b)