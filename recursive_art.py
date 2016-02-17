""" recursive_art.py: randomly generates art """
__author__ = "Gaby Clarke"

import random
from PIL import Image
import math


def buildRandomFunction(minDepth, maxDepth):
    """ Builds a random function of depth at least minDepth and depth
        at most maxDepth (see assignment writeup for definition of depth
        in this context)

        minDepth: the minimum depth of the random function
        maxDepth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    
    functions = ['x', 'y', 't', 'prod', 'avg', 'cosPi', 'sinPi', 'square', 'cube']
    function = random.choice(functions)

    # depth = random.randint(minDepth, maxDepth)
    # # print depth

    # if depth <= 1:
    # 	return [random.choice(['x', 'y', 't'])]
    if function == 'x':
    	return ['x']
    elif function == 'y':
    	return ['y']
    elif function == 't':
    	return ['t']
    elif function == 'prod':
    	return ['prod', buildRandomFunction(minDepth-1, maxDepth-1), buildRandomFunction(minDepth-1, maxDepth-1)]
    elif function == 'avg':
    	return ['avg', buildRandomFunction(minDepth-1, maxDepth-1), buildRandomFunction(minDepth-1, maxDepth-1)]
    elif function == 'cosPi':
    	return ['cosPi', buildRandomFunction(minDepth-1, maxDepth-1)]
    elif function == 'sinPi':
    	return ['sinPi', buildRandomFunction(minDepth-1, maxDepth-1)]
    elif function == 'square':
    	return ['square', buildRandomFunction(minDepth-1, maxDepth-1)]
    elif function == 'cube':
    	return ['cube', buildRandomFunction(minDepth-1, maxDepth-1)]



def evaluateRandomFunction(f, x, y, t):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluateRandomFunction(['x'],-0.5, 0.75)
        -0.5
        >>> evaluateRandomFunction(['y'],0.1,0.02)
        0.02
        >>> evaluateRandomFunction('x',-1,1)
        <type 'exceptions.ValueError'>
    """
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 't':
    	return t
    elif f[0] == 'prod':
    	return evaluateRandomFunction(f[1], x, y, t) * evaluateRandomFunction(f[2], x, y, t)
    elif f[0] == 'avg':
        	return 0.5 * (evaluateRandomFunction(f[1], x, y, t) + evaluateRandomFunction(f[2], x, y, t))
    elif f[0] == 'cosPi':
    	return math.cos(math.pi * evaluateRandomFunction(f[1], x, y, t))
    elif f[0] == 'sinPi':
      	return math.sin(math.pi * evaluateRandomFunction(f[1], x, y, t))
    elif f[0] == 'square':
    	return evaluateRandomFunction(f[1], x, y, t)**2
    elif f[0] == 'cube':
    	return evaluateRandomFunction(f[1], x, y, t)**3
    # else:
    #     return ValueError

    # if f[0] == ['x']:
    #     return x
    # elif f[0] == ['y']:
    #     return y
    # elif f[0] == ['prod']:
    # 	return f[1] * f[2]
    # elif f[0] == ['avg']:
    # 	return 0.5 * f[1] + f[2]
    # elif f[0] == ['cosPi']:
    # 	return math.cos(math.pi * f[1])
    # elif f[0] == ['sinPi']:
    # 	return math.sin(math.pi * f[1])
    # elif f[0] == ['square']:
    # 	return f[1]**2
    # elif f[0] == ['cube']:
    # 	return f[1]**3

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
    # colorCode = remapInterval(val, -1, 1, 0, 255)
    colorCode = remapInterval(val, -1, 1, 0, 255)
    return int(colorCode)


def testImage(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remapInterval(i, 0, x_size, -1, 1)
            y = remapInterval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generateArt(filePrefix, frames, x_size=640, y_size=360):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    framesOG = frames
    frames += 1

    # Functions for red, green, and blue channels - where the magic happens!
    red_function = buildRandomFunction(6, 8)
    green_function = buildRandomFunction(6, 8)
    blue_function = buildRandomFunction(6, 8)

    # Create image and loop over all pixels
    for f in range(1,frames):
	    im = Image.new("RGB", (x_size, y_size))
	    pixels = im.load()
	    for i in range(x_size):
	        for j in range(y_size):
	            x = remapInterval(i, 0, x_size, -1, 1)
	            y = remapInterval(j, 0, y_size, -1, 1)
	            t = remapInterval(f, 0, frames, -1, 1)
	            pixels[i, j] = (
	                    colorMap(evaluateRandomFunction(red_function, x, y, t)),
	                    colorMap(evaluateRandomFunction(green_function, x, y, t)),
	                    colorMap(evaluateRandomFunction(blue_function, x, y, t))
	                    )

		# im2 = im
		im.save(filePrefix + str(f).zfill(3) + '.png')
		if f != framesOG:
			opposite = range(framesOG)[-f]
			im.save(filePrefix + str(opposite+framesOG).zfill(3) + '.png')

if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(remapInterval, globals())

    generateArt('frame12',25)
