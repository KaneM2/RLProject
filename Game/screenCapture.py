import pygame
from PIL import Image
import numpy as np


def getDisplay(display):
    img = pygame.surfarray.array3d(display)

    imgArray = np.array(img)
    gridArray = imgArray[::25, ::25, :]

    red = (gridArray[:, :, 0] == 255) & (gridArray[:, :, 1] == 0) & (gridArray[:, :, 2] == 0)
    green = (gridArray[:, :, 0] == 0) & (gridArray[:, :, 1] == 255) & (gridArray[:, :, 2] == 0)
    blue = (gridArray[:, :, 0] == 0) & (gridArray[:, :, 1] == 0) & (gridArray[:, :, 2] == 255)
    black = (gridArray[:, :, 0] == 0) & (gridArray[:, :, 1] == 0) & (gridArray[:, :, 2] == 0)

    stack = np.stack((1 * red, 1 * green, 1 * blue, 1 * black))
    orderedStack = np.moveaxis(stack, 0, -1)

    return orderedStack
