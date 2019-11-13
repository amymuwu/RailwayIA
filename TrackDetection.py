import cv2 as cv
import numpy as np
import math

image = cv.imread('C:/Users/Amy/OneDrive/Documents/IGEN 330/ref images/baseimage.jpg', cv.IMREAD_GRAYSCALE)
#output variables
edges = cv.Canny(image, 50, 200, None, 3)
edgeimage = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
cdstP = np.copy(edgeimage)

lines = cv.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv.line(edgeimage, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

linesP = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)

cv.imshow("Source", image)
cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", edgeimage)
# cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
cv.waitKey()