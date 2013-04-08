#!/usr/bin/env python

from PIL import Image

class PhotoMosaicInputImage:

    def __init__(self, fileName):
        self.fileName = fileName
        self.image = Image.open(fileName)
        self.averagePixelValues = [0, 0, 0]
