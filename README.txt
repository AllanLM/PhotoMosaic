PhotoMosaic
===========

Experimental Python application to generate photo mosaics

Directions
----------

1. Run PhotoMosaicApp.py.
2. Click the "Select Input Image" button and select a target image. The target image is 
   displayed in the image box on the left side of the application.
3. Click the "Select Input Folder" button and select a folder containing valid images.
4. Click the "Start Processing" button.
5. When processing has completed, the generated photomosaic is displayed in the image box 
   on the right side of the application.
6. Click "Clear Mosaic" to delete the photomosaic, or click "Save Mosaic" to specify a 
   location and filename to save the photomosaic.

To Do List
----------

- Process library folder images more efficiently so that the program does not crash when 
  handling a large number of images.

- Improve the mosaicing algorithm:
    - Develop better method for determining which library image matches best with a given 
      cell in the target image grid.
    - The target image and library folder images are currently all squared for easy 
      processing; the program should allow and handle rectangular images.
    - The target image grid is currently restricted to n x n cells; the program should 
      allow for m x n cells where appropriate.
    - The algorithm currently only handles three image channels; it should handle between
      1 and 4.
    - The algorithm allows a library image to appear more than once in the photomosaic;
      each library image should appear between 0 and 2 times in the photomosaic.

- Replace "Select Input Folder" button with a panel where the user can add individual 
  images, as well as folders full of images. The panel will include a scrollable list 
  and a preview image box. Right-click on an image name in the list to remove it from 
  the list.

- If selecting a folder of input images, provide option to add all sub-folders as well.

- Add command line prompt support (no GUI).

- Use terminology "target image" and "library images" throughout the code for clarity.

- Improve format and substance of comments.

Change Log
----------

04-Nov-2013
    - Input Images frame no longer changes size when input image is displayed
    - Mosaic Results frame no longer changes size when output image is displayed
    - Location of Input File and Input Folder lines in the Input Images frame no longer
      change positions when the input image is displayed

01-Nov-2013
    - Fixed exception when clicking the Clear Mosaic button more than once
    - Error message displayed if input image is invalid instead of exception
    - Error message displayed if input folder does not contain any valid images instead
      of exception
    - List of input images is reset before processing so that multiple jobs can be run 
      properly
