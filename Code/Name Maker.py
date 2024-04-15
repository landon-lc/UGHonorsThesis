# This program automatically generates filenames for 4x4 well-plate images.
# Landon Casstevens
def printer():

    wellCode = str(input("Well plate code: "))
    for x in range(1, 11, 2):
        print('Break')
        print(wellCode + 'A' + str(x) + "," + wellCode + 'B' + str(x) + "," + wellCode + 'A' + str(x+1) + "," + wellCode + 'B' + str(x+1))
        print('Break')
        print(wellCode + 'C' + str(x) + "," + wellCode + 'D' + str(x) + "," + wellCode + 'C' + str(x+1) + "," + wellCode + 'D' + str(x+1))
        print('Break')
        print(wellCode + 'E' + str(x) + "," + wellCode + 'F' + str(x) + "," + wellCode + 'E' + str(x+1) + "," + wellCode + 'F' + str(x+1))

printer()