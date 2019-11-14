import cv2 as cv
import numpy as np
import math

"""Parameters"""
pixels_to_mm = 0.1
track_y = 30 #value to crop top and bottom of the image by
canny_lower_threshold = 150
canny_upper_threshold = 300
HL_rho = 1 #1
HL_theta = 180 #180
HL_threshold = 150 #150
HLP_rho = 1 #1
HLP_theta = 180 #180
HLP_threshold = 50 #150
HLP_min_line_length = 10


"""Reference Image"""
image = cv.imread('C:/Users/Amy/OneDrive/Documents/IGEN 330/ref images/image4.jpg', cv.IMREAD_GRAYSCALE)
image_track = image[track_y: -track_y-30]


def vertical_crack(edges, threshold=1):
    linesP = cv.HoughLinesP(edges, HLP_rho, np.pi / HLP_theta, HLP_threshold, None, HLP_min_line_length, 10)
    xvalues = []
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if l[0] <= l[2] + threshold & l[0] >= l[2] - threshold:
                xvalues.append(l[0])
                xvalues.append(l[2])
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
    try:
        width_of_crack(xvalues)
    except:
        print("no vertical cracks")
        image_track_blur = cv.medianBlur(image_track, 7)
        detect_circle(image_track_blur)


def detect_circle(image_track_blur):
    ##circles
    # HoughCircles(image, method, dp (acc has same resolution of same size), minDist, param1, param2)
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, 70, param1=50, param2=32, minRadius=0,
                              maxRadius=0)

    try:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv.circle(image_track, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv.circle(image_track, (i[0], i[1]), 2, (0, 0, 255), 3)
    except:
        print("no circles found")


def width_of_crack(values):
    width = max(values) - min(values)
    print(width * pixels_to_mm)

#output variables
edges = cv.Canny(image_track, canny_lower_threshold, canny_upper_threshold, None, 3)
edgeimage = cv.cvtColor(edges, cv.COLOR_GRAY2BGR) #to show the canny image in imshow
cdstP = np.copy(edgeimage)

cv.imshow("Canny Transform", edgeimage)

#standard hough transform
#cv2.HoughLines(image, rho - distance resolution of accumulator, theta - angle resolution of accumulator, threshold[, lines[, srn[, stn]]]) → lines
# lines = cv.HoughLines(edges, HL_rho, np.pi/HL_theta, HL_threshold, None, 0, 0) #lines stores the coordinates of start/end line
#
# if lines is not None:
#     for i in range(0, len(lines)):
#         rho = lines[i][0][0]
#         theta = lines[i][0][1]
#         a = math.cos(theta)
#         b = math.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
#         pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
#         cv.line(edgeimage, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

vertical_crack(edges)

cv.imshow('detected circles',image_track)
# cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", edgeimage)
cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
cv.waitKey()