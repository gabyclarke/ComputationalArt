""" recursive_art.py: randomly generates "art" """
__author__ = "Gaby Clarke"

import random
from PIL import Image
from math import cos, sin, pi


def buildRandomFunction(minDepth, maxDepth,):
    """ Builds a random function of depth at least minDepth and depth
        at most maxDepth (see assignment writeup for definition of depth
        in this context)

        minDepth: the minimum depth of the random function
        maxDepth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    x = lambda x, y, t: x
    y = lambda x, y, t: y
    time = lambda x, y, t: t
    baseFunctions = [x, y, time]

    functions = ['cosPi', 'sinPi', 'square', 'cube', 'prod', 'avg']

    if maxDepth <= 1 or (minDepth <= 1 and random.randint(0,1)):
        return random.choice(baseFunctions)
    else:
        f = random.choice(functions)
        recurse = buildRandomFunction(minDepth-1, maxDepth-1)

        if f == 'cosPi':
            return lambda x, y, t: cos(pi * recurse(x, y, t))
        elif f == 'sinPi':
            return lambda x, y, t: sin(pi * recurse(x, y, t))
        elif f == 'square':
            return lambda x, y, t: recurse(x, y, t)**2
        elif f == 'cube':
            return lambda x, y, t: recurse(x, y, t)**3
        elif f == 'prod':
            recurse2 = buildRandomFunction(minDepth-1, maxDepth-1)
            return lambda x, y, t: recurse(x, y, t) * recurse2(x, y, t)
        elif f == 'avg':
            recurse2 = buildRandomFunction(minDepth-1, maxDepth-1)
            return lambda x, y, t: (recurse(x, y, t) + recurse2(x, y, t)) / 2.0


def remapInterval(val,
                   inputIntervalStart,
                   inputIntervalEnd,
                   outputIntervalStart,
                   outputIntervalEnd):
    """ Given an input value in the interval [inputIntervalStart,
        inputIntervalEnd], return an output value scaled to fall within
        the output interval [outputIntervalStart, outputIntervalEnd].

        val: the value to remap
        inputIntervalStart: the start of the interval that contains all
                              possible values for val
        inputIntervalEnd: the end of the interval that contains all possible
                            values for val
        outputIntervalStart: the start of the interval that contains all
                               possible output values
        outputIntervalEnd: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remapInterval(0.5, 0, 1, 0, 10)
        5.0
        >>> remapInterval(5, 4, 6, 0, 2)
        1.0
        >>> remapInterval(5, 4, 6, 1, 2)
        1.5
    """
    inputDelta = inputIntervalEnd - inputIntervalStart
    inputPosition = float(val - inputIntervalStart) / inputDelta
    outputDelta = outputIntervalEnd - outputIntervalStart
    outputPosition = outputIntervalStart + (inputPosition * outputDelta)
    return outputPosition


def colorMap(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> colorMap(-1.0)
        0
        >>> colorMap(1.0)
        255
        >>> colorMap(0.0)
        127
        >>> colorMap(0.5)
        191
    """
    colorCode = remapInterval(val, -1, 1, 0, 255)
    return int(colorCode)


def generateArt(filename, frames, xSize=350, ySize=350):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        xSize, ySize: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    redFunction = buildRandomFunction(7,9)
    greenFunction = buildRandomFunction(7,9)
    blueFunction = buildRandomFunction(7,9)

    for frame in range(frames):
        t = remapInterval(frame, 0, frames, -1, 1)
        # Create image and loop over all pixels
        im = Image.new("RGB", (xSize, ySize))
        pixels = im.load()
        for i in range(xSize):
            for j in range(ySize):
                x = remapInterval(i, 0, xSize, -1, 1)
                y = remapInterval(j, 0, ySize, -1, 1)
                pixels[i, j] = (
                        colorMap(redFunction(x,y,t)),
                        colorMap(greenFunction(x,y,t)),
                        colorMap(blueFunction(x,y,t))
                        )

        im.save(filename + str(frame) + '.png')

if __name__ == '__main__':
    generateArt('test',1)
