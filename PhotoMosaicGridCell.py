#!/usr/bin/env python

class PhotoMosaicGridCell:
    
    def __init__(self, initialX, initialY, width, height):
        self.initialX = initialX
        self.initialY = initialY
        self.width = width
        self.height = height
        self.image = None
        self.averagePixelValues = [0, 0, 0]
        self.score = 999999.0
        self.bestInputImage = None 