import math
import random


# Addition of 2 2D vectors
def sum(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

# Subtraction of 2 2D vectors
def sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

#  Multiplies 2D  vector by a scalar
def mult(v, k):
    return [v[0] * k, v[1] * k]

# Divides 2D vector by a scalar
def div(v, k):
    return [v[0] / k, v[1] / k]

# Calculates the magnitude (length) of the vector and returns the result 
def mag(v):
    return math.sqrt(magSq(v))

# Calculates the squared magnitude of 2D vector
def magSq(v):
    return v[0] * v[0] + v[1] * v[1]

# Normalize the vector to length 1 (make it a unit vector).
def normalize(v):
    length = mag(v)
    if length != 0:
        v = mult(v, 1/length)
    return v

# Limit the magnitude of 2D vector to the value used for the parameter
def limit(v, max):
    mSq = magSq(v)
    if mSq > max * max:
        v = mult(div(v, math.sqrt(mSq)), max)
    return v

# Set the magnitude of this vector to a value
def setMag(v, n):
    return mult(normalize(v), n)