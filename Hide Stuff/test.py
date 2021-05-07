import numpy as np
import cv2 as cv
import random

if __name__ == "__main__":
    filename = "duck.jpg"
    img = cv.imread(filename)
    rows, cols, channels = img.shape

    print("Number of Rows: " + str(rows))
    print("Number of Columns: " + str(cols))
    print("Number of Channels: " + str(channels))

    for y in range(rows):
        for x in range(cols):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            chance = random.randint(0, 10)
            if chance > 9:
                color = (r, g, b)
                img[y,x] = color

    cv.namedWindow('image', cv.WINDOW_AUTOSIZE)
    cv.imshow('image', img)
    cv.waitKey()
    cv.destroyAllWindows()