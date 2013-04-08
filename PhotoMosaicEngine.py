#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import math
from os import listdir, remove
from os.path import isfile, join
from PIL import Image, ImageStat
from Tkinter import Tk
from tkFileDialog import asksaveasfilename
from PhotoMosaicInputImage import PhotoMosaicInputImage
from PhotoMosaicGridCell import PhotoMosaicGridCell

class PhotoMosaicEngine:

    # Find and open the specified target image.
    def findInputImage(self):
        self.inputImage = PhotoMosaicInputImage(self.inputImageFilename)

    # If the image is not already square, crop it down to a square.
    def squareInputImage(self):
        if self.inputImage.image.size[0] != self.inputImage.image.size[1]:
            newDim = min(self.inputImage.image.size)
            self.inputImage.image = self.inputImage.image.resize([newDim, newDim])

    # Calculate the dimensions of the grid for the target image based on the
    # number of available library images.
    def calculateInputGridDimensions(self):
        self.inputGridDim = int(math.sqrt(len(self.inputFolderImages)))

    # Create the grid for the target image.
    def createInputImageGrid(self):
        cellWidth = int(math.floor(self.inputImage.image.size[0] / self.inputGridDim))
        cellHeight = int(math.floor(self.inputImage.image.size[1] / self.inputGridDim))
        
        self.inputGrid = [[0 for x in xrange(self.inputGridDim)] for x in xrange(self.inputGridDim)]
        for i in range(self.inputGridDim):
            for j in range(self.inputGridDim):
                self.inputGrid[i][j] = PhotoMosaicGridCell(i * cellWidth, j * cellHeight, cellWidth, cellHeight)
                self.inputGrid[i][j].image = self.inputImage.image.crop((i * cellWidth, j * cellHeight, (i * cellWidth) + cellWidth, (j * cellHeight) + cellHeight))

    # Calculate the average red, green, and blue values of each cell in the
    # target image.
    def calcInputImageGridAverageRGB(self):
        for i in range(self.inputGridDim):
            for j in range(self.inputGridDim):
                gridCellImageStat = ImageStat.Stat(self.inputGrid[i][j].image)
                self.inputGrid[i][j].averagePixelValues = gridCellImageStat.median

    # Find all valid image files in the specified input folder.
    def findInputFolderImages(self):
        inputFolderFiles = [ f for f in listdir(self.inputFolder) if isfile(join(self.inputFolder,f)) ]
        for inputFolderFile in inputFolderFiles:
            try:
                imageF = Image.open(self.inputFolder + "/" + inputFolderFile)
                imageF.verify()
                pmInputImage = PhotoMosaicInputImage(self.inputFolder + "/" + inputFolderFile)
                self.inputFolderImages.append(pmInputImage)
            except:
                continue
            
    # Make each of the library images square.
    def squareInputFolderImages(self):
        for inputFolderImage in self.inputFolderImages:
            if inputFolderImage.image.size[0] != inputFolderImage.image.size[1]:
                newDim = min(inputFolderImage.image.size)
                inputFolderImage.image = inputFolderImage.image.resize([newDim, newDim])

    # Calculate the average red, green, and blue values of each library image.
    def calcInputFolderImagesAverageRGB(self):
        for inputFolderImage in self.inputFolderImages:
            inputFolderImageStat = ImageStat.Stat(inputFolderImage.image)
            inputFolderImage.averagePixelValues = inputFolderImageStat.median

    # For each cell in the target image grid, find the library image whose pixel
    # values are closest to the pixel values of the cell.
    def matchInputFolderImagesToInputImageGrid(self):
        for i in range(self.inputGridDim):
            for j in range(self.inputGridDim):
                for inputFolderImage in self.inputFolderImages:
                    score = (math.fabs(inputFolderImage.averagePixelValues[0] - self.inputGrid[i][j].averagePixelValues[0]) +
                             math.fabs(inputFolderImage.averagePixelValues[1] - self.inputGrid[i][j].averagePixelValues[1]) + 
                             math.fabs(inputFolderImage.averagePixelValues[2] - self.inputGrid[i][j].averagePixelValues[2]))
                    if (score < self.inputGrid[i][j].score):
                        self.inputGrid[i][j].score = score
                        self.inputGrid[i][j].bestInputImage = inputFolderImage
                        
    # Generate the photomosaic and save it.
    def stitchMosaicTogether(self):
        self.outputImage = Image.new("RGBA", self.inputImage.image.size)

        for i in range(self.inputGridDim):
            for j in range(self.inputGridDim):
                self.outputImage.paste(self.inputGrid[i][j].bestInputImage.image, (self.inputGrid[i][j].initialX, self.inputGrid[i][j].initialY))

        self.outputImage.save(self.outputImageFilename)        

    def generateMosaic(self):
        self.outputImageFilename = "outputImage.jpg"

        # Most of these steps can be combined, but I've left them separate to
        # make the process clearer.
        self.findInputImage()
        self.squareInputImage()

        self.findInputFolderImages()
        self.squareInputFolderImages()
        self.calcInputFolderImagesAverageRGB()

        self.calculateInputGridDimensions()
        self.createInputImageGrid()
        self.calcInputImageGridAverageRGB()

        self.matchInputFolderImagesToInputImageGrid()
        self.stitchMosaicTogether()

    # Delete the generated photomosaic.
    def deleteOutput(self):
        remove(self.outputImageFilename)
        self.outputImage = None

    # Save the generated photomosaic.
    def saveOutput(self):
        Tk().withdraw()
        selectedFileName = asksaveasfilename()
        self.outputImage.save(selectedFileName)

    def __init__(self):
        self.inputImageFilename = ""
        self.inputImage = None

        self.inputFolder = ""
        self.inputFolderImages = []

        self.inputGridDim = 0
        self.inputGrid = None

        self.outputImage = None
        self.outputImageFilename = ""

