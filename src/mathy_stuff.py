"""
Mathy stuff for Some Platformer Game
Created by duuuck and sheepy0125
22/10/2021
"""


def ccw(A, B, C):
    """Check if three points are in counter clockwise order"""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def line_intersection(line1, line2):
    """Find the intersection between two lines"""

    # Check if the lines are in counter clockwise order
    if ccw(line1[0], line1[1], line2[0]) == ccw(line1[0], line1[1], line2[1]):
        return None
    if ccw(line2[0], line2[1], line1[0]) == ccw(line2[0], line2[1], line1[1]):
        return None

    # Calculate the slope of the lines
    m1 = (line1[1][1] - line1[0][1]) / (line1[1][0] - line1[0][0])
    m2 = (line2[1][1] - line2[0][1]) / (line2[1][0] - line2[0][0])

    # Calculate the y-intercepts of the lines
    b1 = line1[0][1] - m1 * line1[0][0]
    b2 = line2[0][1] - m2 * line2[0][0]

    # Calculate the x-intercepts of the lines
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x

    # Debug print in slope intercept form
    print(f"Line 1: y={m1}x + {b1}")
    print(f"Line 2: y={m2}x + {b2}")
    print(f"Intersection: ({x}, {y})")

    return (x, y)
