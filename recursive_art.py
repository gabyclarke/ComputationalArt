""" recursive_art.py: randomly generates "art" """
__author__ = "Gaby Clarke"

import random
from PIL import Image
from math import cos, sin, pi

import inspect

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

    # cosPi = lambda x: cos(pi * x)
    # sinPi = lambda x: sin(pi * x)
    # square = lambda x: x**2
    # cube = lambda x: x**3
    # oneArgFunctions = [cosPi, sinPi, square, cube]
    
    # prod = lambda x, y: x * y
    # avg = lambda x, y: (x + y) / 2.0
    # twoArgFunctions = [prod, avg]

    functions = ['cosPi', 'sinPi', 'square', 'cube', 'prod', 'avg']



    if maxDepth <= 1 or (minDepth <= 1 and random.randint(0,1)):
        return random.choice(baseFunctions)
    else:
        f = random.choice(functions)
        # arguments = random.randint(0,5)
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

        # recurse2 = buildRandomFunction(minDepth-1, maxDepth-1)
        # if arguments == 1:
        #     f = random.choice(oneArgFunctions)
        #     return lambda x, y, t: f(recurse(x, y, t))
        # elif arguments == 2:
        #     f = random.choice(twoArgFunctions)
        #     return lambda x, y, t: f(recurse(x, y, t), recurse2(x, y, t))
            


# def buildRandomFunction(minDepth, maxDepth,):
#     """ Builds a random function of depth at least minDepth and depth
#         at most maxDepth (see assignment writeup for definition of depth
#         in this context)

#         minDepth: the minimum depth of the random function
#         maxDepth: the maximum depth of the random function
#         returns: the randomly generated function represented as a nested list
#                  (see assignment writeup for details on the representation of
#                  these functions)
#     """

#     oneArgFunctions = {
#         'cosPi': lambda x: cos(pi * x),
#         'sinPi': lambda x: sin(pi * x),
#         'square': lambda x: x**2,
#         'cube': lambda x: x**3,
#     }

#     twoArgFunctions = {
#         'prod': lambda x, y: x * y, 
#         'avg': lambda x, y: (x + y) / 2.0,
#     }

#     baseFunctions = {
#         'x': lambda x, y, t: x,
#         'y': lambda x, y, t: y,
#         't': lambda x, y, t: t,
#     }
    
#     if maxDepth <= 1 or (minDepth <= 1 and random.randint(0,1)):
#         # print 'base'
#         fKey = random.choice(baseFunctions.keys())
#         f = baseFunctions[fKey]
#         return f
#     else:
#         arguments = random.randint(1,2)
#         recurse = buildRandomFunction(minDepth-1, maxDepth-1)
#         recurse2 = buildRandomFunction(minDepth-1, maxDepth-1)
#         # recurse3 = buildRandomFunction(minDepth-1, maxDepth-1)
#         if arguments == 1:
#             # print 1
#             fKey = random.choice(oneArgFunctions.keys())
#             f = oneArgFunctions[fKey]
#             # print inspect.getsource(f)
#             # print inspect.getsource(recurse)
#             # print inspect.getsource(f(recurse))
#             return lambda x, y,t: f(recurse(x, y,t))
#         elif arguments == 2:
#             # print 2
#             fKey = random.choice(twoArgFunctions.keys())
#             f = twoArgFunctions[fKey]
#             return lambda x, y,t: f(recurse(x, y,t),recurse2(x,y,t))
#             # return lambda x, y, t: f(recurse(x, y, t), recurse2(x, y, t))
#             # return f(recurse, recurse2)
#             # return lambda x, y, t: f(recurse(x, y, t), recurse2(x, y, t), recurse3(x, y, t))




#         # fKey = random.choice(functions.keys())
#         # f = functions[fKey]
#         # return lambda x, y, t: f(recurse(x, y, t), recurse(x, y, t))



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


# def generateArt(filePrefix, frames, x_size=640, y_size=360):
#     """ Generate computational art and save as an image file for compilation as a video.
#     	This function generates two versions of the same image with different file names,
#     	such that you can generate a looping video.

#         filename: string filename for image (should be .png)
#         x_size, y_size: optional args to set image dimensions (default: 350)
#     """
#     framesCopy = frames
#     frames += 1

#     # Functions for red, green, and blue channels - where the magic happens!
#     redFunction = buildRandomFunction(3, 5)
#     greenFunction = buildRandomFunction(3, 5)
#     blueFunction = buildRandomFunction(3, 5)

#     # print inspect.getsource(redFunction)
#     # Create image and loop over all pixels
#     for f in range(1,frames):
# 	    im = Image.new("RGB", (x_size, y_size))
# 	    pixels = im.load()
# 	    for i in range(x_size):
# 	        for j in range(y_size):
# 	            x = remapInterval(i, 0, x_size, -1, 1)
# 	            y = remapInterval(j, 0, y_size, -1, 1)
# 	            t = remapInterval(f, 0, frames, -1, 1)
#                 pixels[i, j] = (
#                     colorMap(redFunction(x, y, t)),
#                     colorMap(greenFunction(x, y, t)),
#                     colorMap(blueFunction(x, y, t))
#                     )
#                 print pixels[i,j]

# 		im.save(filePrefix + str(f).zfill(3) + '.png')
# 		if f != framesCopy:
# 			opposite = range(framesCopy)[-f]
# 			im.save(filePrefix + str(opposite+framesCopy).zfill(3) + '.png')

def generateArt(filename, frames, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = buildRandomFunction(7,9)
    green_function = buildRandomFunction(7,9)
    blue_function = buildRandomFunction(7,9)

    for frame in range(frames):
        t = remapInterval(frame, 0, frames, -1, 1)
        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                x = remapInterval(i, 0, x_size, -1, 1)
                y = remapInterval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        colorMap(red_function(x,y,t)),
                        colorMap(green_function(x,y,t)),
                        colorMap(blue_function(x,y,t))
                        )

        im.save(filename + str(frame) + '.png')

if __name__ == '__main__':
    generateArt('tests',1)
