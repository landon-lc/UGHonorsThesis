# Written by Landon Casstevens

"""
NOTES

.tif files will interpret 'transparent' spaces as black pixels - 0, 0, 0 for RGB values.

CE2-Cropped performs well with 30% thresholding across all channels. At 10% it is good, but
it picks up a significant amount of the fingerprint/wave pattern at the bottom. This is a stark contrast from
CE3-Cropped, where 5% thresholding performs much better. This could potentially be automated via corner detection.

Sobel size must be odd.
"""

"""
RESOURCES

Erosion and Dialation (OpenCV) - https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
Erosion and Dialation Example (GforG) - https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
Edge Detection - https://en.wikipedia.org/wiki/Edge_detection
Canny Edge Detection - https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
"""

import cv2
import numpy as np
import os

def main():

    # Select one

    multiImageRun()
    #singleImageRun()

def multiImageRun():

    imageList = []
    for file in os.listdir():
        if file.endswith(".tif"):
            imageList.append(file)

    for imageIndex in range(len(imageList)-1):
        userInputIMG = cv2.imread(imageList[imageIndex])
        bluAvg, grnAvg, redAvg, totalArea = channelAverage(userInputIMG)
        percArea, finalIMG = areaByChannels(.20, .05, .05, bluAvg, grnAvg, redAvg, userInputIMG, totalArea, False)
        cannyArea = cannyFinder(userInputIMG, 25, 175, False, totalArea)
        finalCrystalArea = percArea * 100
        finalCannyArea = cannyArea * 100

        # Easy to read formatting
        # print("\nData for image:  " + imageList[imageIndex])
        # print("\tCrystal Pixel Area: " + "%.2f" % (finalCrystalArea))
        # print("\tCanny Edges Area: " + "%.2f" % (finalCannyArea))
        # print("\tCategory: " + crystalCategorizer(finalCrystalArea, finalCannyArea))

        # Raw Excel Output
        # print(crystalCategorizer(finalCrystalArea, finalCannyArea) + "\t" + "%.2f" % (finalCrystalArea) + "\t" + "%.2f" % (finalCannyArea))

        # Excel (extra) Formatting
        print(imageList[imageIndex] + "\t" + crystalCategorizer(finalCrystalArea, finalCannyArea) + "\t" + "%.2f" % (finalCrystalArea) + "\t" + "%.2f" % (finalCannyArea))

        # Sample Formatting
        # print(imageList[imageIndex] + "\t" + crystalCategorizer(finalCrystalArea, finalCannyArea) + "\t" + "%.2f" % (finalCannyArea) + "\t" + "%.2f" % (finalCrystalArea))
def crystalCategorizer(crystalArea, cannyArea):

    # Categorizes a crystal into 1 of 4 categories based on two area values.

    if 0 <= cannyArea < 20 and 14.8 <= crystalArea < 23:
        return 'Abundant Crystal'
    if 0 <= cannyArea < 20 and 14.8 > crystalArea:
        return 'Sparse Crystal'
    if 0 <= cannyArea < 22 and 23 <= crystalArea < 39:
        return 'Sparse Aggregate'
    if 20 <= cannyArea < 22 and 19 <= crystalArea < 23 or 20 <= cannyArea < 38 and 19 <= crystalArea < 39:
        return 'Abundant Aggregate'
    else:
        return 'Categorization out of bounds.'

def singleImageRun():

    userInputIMG = importer()
    bluAvg, grnAvg, redAvg, totalArea = channelAverage(userInputIMG)
    percArea, finalIMG = areaByChannels(.20, .05, .05, bluAvg, grnAvg, redAvg, userInputIMG, totalArea, True)
    # eRo, dIl = eroderDilator(userInputIMG, 3, 3, 1, 1)

    cannyArea = cannyFinder(userInputIMG, 25, 175, True, totalArea)
    # harrisCorners(userInputIMG, 3, 7, 0, .05)

    finalCrystalArea = percArea * 100
    finalCannyArea = cannyArea * 100
    print("\tCrystal Pixel Area: " + "%.2f" % (finalCrystalArea))
    print("\tCanny Edges Area: " + "%.2f" % (finalCannyArea))
    print("\tCategory: " + crystalCategorizer(finalCrystalArea, finalCannyArea))

    cv2.imshow("Input Image", userInputIMG/255)
    cv2.imshow("Final Image", finalIMG/255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def harrisCorners(inputIMG, neighborhood, sobelSize, harrisFree, displayBool):

    harrisPrepIMG = cv2.cvtColor(inputIMG, cv2.COLOR_BGR2GRAY)
    harrisOutputIMG = cv2.cornerHarris(src=harrisPrepIMG, blockSize=neighborhood, ksize=sobelSize, k=harrisFree)

    if displayBool:
        cv2.imshow("harris", harrisOutputIMG/255)

    return

def cannyFinder(inputIMG, minVal, maxVal, displayBool, totalArea):

    # Finds and displays canny edges.

    cannyIMG = inputIMG.copy()
    resultIMG = cv2.Canny(cannyIMG, minVal, maxVal)
    cannyPixels = 0

    if displayBool:
        cv2.imshow("Canny Output", resultIMG/255)

    for X in range(0, resultIMG.shape[1]):
        for Y in range(0, resultIMG.shape[0]):
            pixelVal = resultIMG[Y][X]
            if pixelVal > 0.5:
                cannyPixels += 1

    return cannyPixels/totalArea

def eroderDilator(givenIMG, eKernSize, dKernSize, eIter, dIter):

    # Provides an Eroded and Dialated image.

    interIMG = givenIMG.copy()
    finalIMG = cv2.cvtColor(interIMG, cv2.COLOR_BGR2GRAY)
    finalIMG2 = finalIMG.copy()

    erosionKernel = np.ones((eKernSize, eKernSize), np.uint8)
    dilationKernel = np.ones((dKernSize, dKernSize), np.uint8)

    eroded = cv2.erode(finalIMG, erosionKernel, iterations = eIter)
    dilated = cv2.dilate(finalIMG2, dilationKernel, iterations = dIter)

    return eroded, dilated

def areaByChannels(bluThresh, grnThresh, redThresh, bluAvg, grnAvg, redAvg, inputIMG, totalArea, drawBool):

    # Gives the % area of the image covered by crystal pixels. Discriminates by color channel using thresholds
    # and average brightness. If drawBool, draws crystals in red.

    finalIMG = inputIMG.copy()

    bluThresh += 1
    grnThresh += 1
    redThresh += 1

    bluMinBright = bluThresh * bluAvg
    grnMinBright = grnThresh * grnAvg
    redMinBright = redThresh * redAvg

    crystalArea = 0

    for X in range(0, finalIMG.shape[1]):
        for Y in range(0, finalIMG.shape[0]):

            BluVal = (finalIMG[Y][X][0])
            GrnVal = (finalIMG[Y][X][1])
            RedVal = (finalIMG[Y][X][2])

            if BluVal >= bluMinBright and GrnVal >= grnMinBright and RedVal >= redMinBright:
                # Pixel is a crystal.
                crystalArea += 1
                if drawBool:
                    finalIMG[Y][X][0] = 0
                    finalIMG[Y][X][1] = 0
                    finalIMG[Y][X][2] = 255

    return (crystalArea/totalArea), finalIMG

def channelAverage(inputIMG):

    # Finds the average brightness for each color channel within the image.

    bluSum = 0
    grnSum = 0
    redSum = 0

    applicableCount = 0
    totalArea = 0

    for X in range(0, inputIMG.shape[1]):
        for Y in range(0, inputIMG.shape[0]):

            BluVal = (inputIMG[Y][X][0])
            GrnVal = (inputIMG[Y][X][1])
            RedVal = (inputIMG[Y][X][2])

            if BluVal != 0 and GrnVal != 0 and RedVal != 0:
                applicableCount += 1
                totalArea += 1
                bluSum += BluVal
                grnSum += GrnVal
                redSum += RedVal

    bluAvg = bluSum / applicableCount
    grnAvg = grnSum / applicableCount
    redAvg = redSum / applicableCount

    return bluAvg, grnAvg, redAvg, totalArea

def importer():
    '''This function handles importing of an image. '''

    ImageName = input("Please enter the name of the image to be edited: ")
    GivenIMG = cv2.imread(ImageName, cv2.IMREAD_UNCHANGED)

    return GivenIMG

main()