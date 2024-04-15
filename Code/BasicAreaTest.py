# All 'transparent' pixels or alpha-channel pixels will read as 000 for RGB values.

import cv2
import numpy as np
import math

def main():
    CurrentIMG = importer()
    # colorChannelDisplay(CurrentIMG)
    # bright = int(input("Please enter the brightnessMOD: "))

    # outputIMG = tester(CurrentIMG, bright)
    # Printing Output
    # cv2.imshow("Input Image", CurrentIMG/255)
    # cv2.imshow("Output Image", outputIMG/255)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # BULK TESTER - FOR 0-255 TESTS
    for brCount in range(0, 256):
        tester(CurrentIMG, brCount)

def tester(mainIMG, brightnessMOD):
    '''
    brightnessMOD is the R, G, and B value from 0 to 255 that must exist. It determines how 'white' a pixel must be
    to be determined part of the crystal.
    '''

    TotalPixels = 0
    CrystalPixels = 0
    DrawToIMG = blankMaker(mainIMG)

    # Loop through image.
    for X in range(0, mainIMG.shape[1]):
        for Y in range(0, mainIMG.shape[0]):

            # Collecting RGB Values
            BluVal = (mainIMG[Y][X][0])
            RedVal = (mainIMG[Y][X][1])
            GrnVal = (mainIMG[Y][X][2])

            if BluVal != 0 and RedVal != 0 and GrnVal != 0:
                # Pixel is part of the original well-plate photo, not a transparent background part.
                # Total pixels in the well plate incremented by 1.
                TotalPixels += 1
                if BluVal >= brightnessMOD and RedVal >= brightnessMOD and GrnVal >= brightnessMOD:
                    # This pixel is considered part of the crystal. A red pixel will be drawn.
                    CrystalPixels += 1
                    DrawToIMG[Y][X][1] = 255
                else:
                    # Not a crystal pixel, white pixel will be drawn.
                    DrawToIMG[Y][X][0] = 255
                    DrawToIMG[Y][X][1] = 255
                    DrawToIMG[Y][X][2] = 255

    CrystalArea = round((((CrystalPixels/TotalPixels)*100)), 2)
    # Pretty Printout
    # print("\nTotal Pixels: " + str(TotalPixels) + "\nCrystal Pixels: " + str(CrystalPixels) + "\nRelative Area: " + str(CrystalArea) + "%")
    # Excel Printout
    print(str(brightnessMOD) + "\t" + str(TotalPixels) + "\t" + str(CrystalPixels) + "\t" + str(CrystalArea))

    return DrawToIMG

# Helper Functions to assist in image intake and other tasks.

def blankMaker(inputIMG):
    '''This function creates a blank (black-pixel) image of equal size to the original.'''

    imgHeight = inputIMG.shape[0]
    imgWidth = inputIMG.shape[1]
    NewIMG = np.zeros((imgHeight, imgWidth, 3), np.float32)

    return NewIMG

def importer():
    '''This function handles importing of an image. '''

    ImageName = input("Please enter the name of the image to be edited: ")
    GivenIMG = cv2.imread(ImageName, cv2.IMREAD_UNCHANGED)

    return GivenIMG

main()
