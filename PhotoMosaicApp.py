#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory
from PhotoMosaicEngine import PhotoMosaicEngine

class PhotoMosaicApp:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    # Present a file select dialog box to the user.
    # The user selects the target image.
    def selectInputFilename_cb(self, widget, data=None):
        Tk().withdraw()
        selectedFileName = askopenfilename()
        if selectedFileName != '':
            self.photoMosaicEngine.inputImageFilename = selectedFileName
            self.lblInputFilename.set_text("Input File: " + self.photoMosaicEngine.inputImageFilename)
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.photoMosaicEngine.inputImageFilename, 600, 400)
            self.inputImage.set_from_pixbuf(pixbuf)
            if self.photoMosaicEngine.inputImageFilename != "" and self.photoMosaicEngine.inputFolder != '':
                self.btnStartProcess.set_sensitive(True)

    # Present a folder select dialog box to the user.
    # The user selects the folder containing the library images for the mosaic.
    # Only use the files that have been verified as actual images.
    def selectInputFolder_cb(self, widget, data=None):
        Tk().withdraw()
        selectedFolder = askdirectory()
        if selectedFolder != '':
            self.photoMosaicEngine.inputFolder = selectedFolder
            self.lblInputFolder.set_text("Input Folder: " + self.photoMosaicEngine.inputFolder)
            if self.photoMosaicEngine.inputImageFilename != "" and self.photoMosaicEngine.inputFolder != '':
                self.btnStartProcess.set_sensitive(True)

    # Call the mosaicing engine. Once the processing has finished, present the results in the frame on the right.
    def startProcess_cb(self, widget, data=None):
        self.photoMosaicEngine.generateMosaic()
        if self.photoMosaicEngine.outputImageFilename != "":
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.photoMosaicEngine.outputImageFilename, 600, 400)
            self.outputImage.set_from_pixbuf(pixbuf)
            self.btnClearOutput.set_sensitive(True)
            self.btnSaveOutput.set_sensitive(True)

    # Delete the generated photomosaic and clear the preview image box.
    def clearOutput_cb(self, widget, data=None):
        self.photoMosaicEngine.deleteOutput()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size("defaultOutputImage.jpg", 600, 400)
        self.outputImage.set_from_pixbuf(pixbuf)
        self.btnSaveOutput.set_sensitive(False)

    # Save the generated photomosaic with a user-specified filename.
    def saveMosaic_cb(self, widget, data=None):
        self.photoMosaicEngine.saveOutput()

    # Draw the input frame on the left side of the application.
    def drawLeftFrame(self):
        frameLeft = gtk.Frame("Input Images")
        frameLeft.set_shadow_type(gtk.SHADOW_IN)
        boxLeft = gtk.VBox(False, 0)
        self.inputImage = gtk.Image()
        pixbufin = gtk.gdk.pixbuf_new_from_file_at_size("defaultInputImage.jpg", 600, 400)
        self.inputImage.set_from_pixbuf(pixbufin)
        boxLeft.pack_start(self.inputImage, False, False, 10)
        self.inputImage.show()
        boxInputFilename = gtk.HBox(False, 0)
        self.lblInputFilename = gtk.Label("Input File: <not yet selected>")
        boxInputFilename.pack_start(self.lblInputFilename, False, False, 10)
        self.lblInputFilename.show()
        self.btnSelectInputFilename = gtk.Button("Select Input Image")
        boxInputFilename.pack_end(self.btnSelectInputFilename, False, False, 10)
        self.btnSelectInputFilename.show()
        boxLeft.pack_start(boxInputFilename, False, False, 10)
        boxInputFilename.show()
        boxInputFolder = gtk.HBox(False, 0)
        self.lblInputFolder = gtk.Label("Input Folder: <not yet selected>")
        boxInputFolder.pack_start(self.lblInputFolder, False, False, 10)
        self.lblInputFolder.show()
        self.btnSelectInputFolder = gtk.Button("Select Input Folder")
        boxInputFolder.pack_end(self.btnSelectInputFolder, False, False, 10)
        self.btnSelectInputFolder.show()
        boxLeft.pack_start(boxInputFolder, False, False, 10)
        boxInputFolder.show()
        frameLeft.add(boxLeft)
        boxLeft.show()
        self.boxMain.pack_start(frameLeft, False, False, 10)
        frameLeft.show()

    # Draw the output frame on the right side of the application.
    def drawRightFrame(self):
        frameRight = gtk.Frame("Mosaic Results")
        frameRight.set_shadow_type(gtk.SHADOW_IN)
        boxRight = gtk.VBox(False, 0)
        self.outputImage = gtk.Image()
        pixbufout = gtk.gdk.pixbuf_new_from_file_at_size("defaultOutputImage.jpg", 600, 400)
        self.outputImage.set_from_pixbuf(pixbufout)
        boxRight.pack_start(self.outputImage, False, False, 10)
        self.outputImage.show()
        boxRightButtons = gtk.HBox(False, 0)
        self.btnStartProcess = gtk.Button("Start Processing")
        self.btnStartProcess.set_sensitive(False)
        self.btnClearOutput = gtk.Button("Clear Mosaic")
        self.btnClearOutput.set_sensitive(False)
        self.btnSaveOutput = gtk.Button("Save Mosaic")
        self.btnSaveOutput.set_sensitive(False)
        boxRightButtons.pack_start(self.btnStartProcess, True, True, 10)
        boxRightButtons.pack_start(self.btnClearOutput, True, True, 10)
        boxRightButtons.pack_end(self.btnSaveOutput, True, True, 10)
        self.btnStartProcess.show()
        self.btnClearOutput.show()
        self.btnSaveOutput.show()
        boxRight.pack_start(boxRightButtons, False, False, 10)
        boxRightButtons.show()
        frameRight.add(boxRight)
        boxRight.show()
        self.boxMain.pack_end(frameRight, False, False, 10)
        frameRight.show()

    def connectCallBacks(self):
        self.btnSelectInputFilename.connect("clicked", self.selectInputFilename_cb, "Select Input Filename")
        self.btnSelectInputFolder.connect("clicked", self.selectInputFolder_cb, "Select Input Folder")
        self.btnStartProcess.connect("clicked", self.startProcess_cb, "Start Process")
        self.btnClearOutput.connect("clicked", self.clearOutput_cb, "Clear Output")
        self.btnSaveOutput.connect("clicked", self.saveMosaic_cb, "Save Mosaic")

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.boxMain = gtk.HBox(False, 0)
        self.drawLeftFrame()
        self.drawRightFrame()
        self.window.add(self.boxMain)
        self.boxMain.show()

        self.connectCallBacks()

        self.photoMosaicEngine = PhotoMosaicEngine()

        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    photoMosaicApp = PhotoMosaicApp()
    photoMosaicApp.main()
