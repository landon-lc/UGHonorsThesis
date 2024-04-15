# All 'transparent' pixels or alpha-channel pixels will read as 000 for RGB values.
# NOTE - This code is specifically changed & optomized to run area analysis on specific color channels.

# Computation Stats for CE2-Blu.png
# Transitioned from pure image calculation (2d image, 255x runs) to array calculation (1d array, 255x runs).
# Brute - 15:37, 1st Optimization - 2:43, 2nd Optimization - 2:40


import cv2
import numpy as np
import math

def main():

    CurrentIMG = importer()
    CurrentIMG = BackToBlack(CurrentIMG)

    print("IMAGE CODE - ENSURE CORRECT BEFORE RUNNING")
    print("1 = Blue Channel, 2 = Green Channel, 3 = Red Channel")
    imageColorCode = int(input("Please enter the code: "))

    theArray = imageToArray(CurrentIMG, imageColorCode)
    totPixels = TotalWellplatePixels(CurrentIMG, imageColorCode)
    upperBound = len(theArray)

    # BULK TESTER - FOR 0-255 TESTS
    for brCount in range(0, 256):
        channelArea(brCount, imageColorCode, theArray, totPixels, upperBound)

    return

def imageToArray(inputIMG, colorChannelCode):
    # This function converts the image to a 1-D array to optomize the area search.
    # X and Y values are irrelevant in this core of this program.

    imageArray = []

    for X in range(0, inputIMG.shape[1]):
        for Y in range(0, inputIMG.shape[0]):
            BluVal = (inputIMG[Y][X][0])
            GrnVal = (inputIMG[Y][X][1])
            RedVal = (inputIMG[Y][X][2])

            if colorChannelCode == 1 and BluVal != 0:
                imageArray.append(BluVal)
            if colorChannelCode == 2 and GrnVal != 0:
                imageArray.append(GrnVal)
            if colorChannelCode == 3 and RedVal != 0:
                imageArray.append(RedVal)

    return imageArray

def channelArea(brightnessMOD, imageColorCode, theArray, TotalPixels, upperBound):
    '''
    brightnessMOD is the R, G, and B value from 0 to 255 that must exist. It determines how 'white' a pixel must be
    to be determined part of the crystal.
    '''

    CrystalPixels = 0

    # Loop through the array.
    for X in range(0, upperBound):
        colorValue = theArray[X]
        if colorValue >= brightnessMOD:
            CrystalPixels += 1

    CrystalArea = round((((CrystalPixels/TotalPixels)*100)), 2)

    # Excel Printout
    print(str(brightnessMOD) + "\t" + str(TotalPixels) + "\t" + str(CrystalPixels) + "\t" + str(CrystalArea))

    return

# Helper Functions to assist in image intake and other tasks.

def TotalWellplatePixels(inputIMG, channelCodeNum):
    # This function determines the number of pixels that make up the well-plate, and not the transparent/black/white
    # background surrounding the well-plate. This number will be fixed throughout computation.

    TotalPixels = 0

    for X in range(0, inputIMG.shape[1]):
        for Y in range(0, inputIMG.shape[0]):

            # Collecting RGB Values
            BluVal = (inputIMG[Y][X][0])
            GrnVal = (inputIMG[Y][X][1])
            RedVal = (inputIMG[Y][X][2])

            # ONLY FOR Blue Image - Uses all blue color channel.
            if channelCodeNum == 1:
                if BluVal != 0:
                    TotalPixels += 1

            # ONLY FOR Green Image - Uses all green color channel.
            if channelCodeNum == 2:
                if GrnVal != 0:
                    TotalPixels += 1

            # ONLY FOR Red Image - Uses all red color channel.
            if channelCodeNum == 3:
                if RedVal != 0:
                    TotalPixels += 1

    return TotalPixels

def BackToBlack(inputIMG):
    # This function converts the pure white pixels bordering an image to black, to ensure
    # correct area calculations are performed.

    returnIMG = inputIMG

    # Loop through image.
    for X in range(0, inputIMG.shape[1]):
        for Y in range(0, inputIMG.shape[0]):

            # Gathering color values.
            BluVal = (inputIMG[Y][X][0])
            GrnVal = (inputIMG[Y][X][1])
            RedVal = (inputIMG[Y][X][2])

            # Check for pure white pixel
            if BluVal == 255 and GrnVal == 255 and RedVal == 255:
                # Pixel is pure white. Set to pure black.
                returnIMG[Y][X][0] = 0
                returnIMG[Y][X][1] = 0
                returnIMG[Y][X][2] = 0

    return returnIMG

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