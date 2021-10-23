"""
Mathy stuff for Some Platformer Game
Created by duuuck and sheepy0125
22/10/2021
"""

# Write a function that finds if two points are in counter clockwise order
def ccw(A, B, C):
    """
    Check if three points are in counter clockwise order
    """
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


# Write a function that finds the cross product of two vectors
# The cross product is a vector perpendicular to both vectors
# A vector is represented by a tuple with two integers
# Use the ccw function to check if the points are in counter clockwise order
def cross_product(A, B):
    """
    Find the cross product of two vectors
    """
    if ccw(A, B, (0, 0)):
        return (A[0] * B[1] - A[1] * B[0], A[1] * B[0] - A[0] * B[1])
    else:
        return (A[0] * B[1] + A[1] * B[0], A[1] * B[0] + A[0] * B[1])
