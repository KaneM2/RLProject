import pygame
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [1, 0.66, 0.33])


def getDisplay(display,screenSize,rows):
    step=int(screenSize/rows)
    img = pygame.surfarray.array3d(display)
    gray=rgb2gray(img)

    grayArray = np.array(gray)
    gridArray = grayArray[::step, ::step]



    return gridArray
