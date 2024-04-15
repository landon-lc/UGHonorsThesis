import cv2
import numpy as np
import math

def main():

    InputIMG = importer()
    colorChannelDisplay(InputIMG)

def colorChannelDisplay(mainIMG):
    '''This function displays the Red, Green, and Blue color channels of an image individually. The values of the
    channel being displayed are unchanged, and the other two channels have their values set to zero (NOTE that this
    is done in a new image, not modifiying the original.'''

    # NOTE - BGR Format is used here.
    # Creates 3 new blank images.
    BluIMG = blankMaker(mainIMG)
    GrnIMG = blankMaker(mainIMG)
    RedIMG = blankMaker(mainIMG)
    # Sets images to white for better contrast.
    BluIMG.fill(255)
    GrnIMG.fill(255)
    RedIMG.fill(255)


    for X in range(0, mainIMG.shape[1]):
        for Y in range(0, mainIMG.shape[0]):

            # Collecting RGB Values
            BluVal = (mainIMG[Y][X][0])
            GrnVal = (mainIMG[Y][X][1])
            RedVal = (mainIMG[Y][X][2])

            if BluVal != 0 and GrnVal != 0 and RedVal != 0:
                # Setting red image.
                BluIMG[Y][X][0] = BluVal
                BluIMG[Y][X][1] = 0
                BluIMG[Y][X][2] = 0
                # Green.
                GrnIMG[Y][X][0] = 0
                GrnIMG[Y][X][1] = GrnVal
                GrnIMG[Y][X][2] = 0
                # Blue.
                RedIMG[Y][X][0] = 0
                RedIMG[Y][X][1] = 0
                RedIMG[Y][X][2] = RedVal

            # For printing original image with white background format.
            if BluVal == 0 and GrnVal == 0 and RedVal == 0:
                mainIMG[Y][X][0] = 255
                mainIMG[Y][X][1] = 255
                mainIMG[Y][X][2] = 255

    print("Color Channels Finished")

    # Printing Output
    #cv2.imshow("Original Image", mainIMG/255)
    #cv2.imshow("Blue Image", BluIMG/255)
    #cv2.imshow("Green Image", GrnIMG/255)
    #cv2.imshow("Red Image", RedIMG/255)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Save Names
    cv2.imwrite("CE#-Src.png", mainIMG)
    cv2.imwrite("CE#-Blu.png", BluIMG)
    cv2.imwrite("CE#-Grn.png", GrnIMG)
    cv2.imwrite("CE#-Red.png", RedIMG)

    return

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