# Drew Simmons
# 10/30/21
# Main_pb
from typing import Union, Any
from matplotlib import pyplot as plt


import cv2
import numpy as np

capture = cv2.VideoCapture(0)  # select camera that the program will use

waitTothrow = 0

while True:
    isTrue, frame = capture.read()
    lower_ir = np.array([220, 220, 220])  # setting the high and low BGR (not RGB) values
    upper_ir = np.array([255, 255, 255])  # brightest pixels have highest values from 0-255

    mask = cv2.inRange(frame, lower_ir, upper_ir)  # creates mask
    kernel = np.ones((5, 5), np.uint8)  # creates 3x3 square kernel for morphology
    mask = cv2.erode(mask, kernel, iterations=1)  # erodes mask with 3x3 square
    mask = cv2.dilate(mask, kernel, iterations=1)  # dilates mask with 3x3 square

#    print(mask)
#    print(len(mask))
#    print(len(mask[0]))

    M = cv2.moments(mask)

    if M["m00"] > 0:  # if there is ir light in the frame take the average
        avgX = int(M["m10"] / M["m00"])
        avgY = int(M["m01"] / M["m00"])
    else:  # if there is not ir light in the frame don't (dividing by 0 is bad)
        avgX = 1
        avgY = 1


# attempt using histogram
    hist = cv2.calcHist([mask], [0], None, [256], [0, 256])
    plt.hist(hist.ravel(), 256, [0, 256]);
    plt.show()


# attempt using contours and open CV library functions
#     contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(frame, contours, 0, (0,255,0),3)


    # this is the attempt at itterating through the matrix below
    # print(avgY)

    # upperArray = 0
    # lowerArray = 0

    # for i in range(len(mask)):
    #     for j in range(len(mask[0])):
    #         if mask[i][j] != 0:
    #             if j < avgY:
    #                 upperArray = upperArray + 1
    #         if mask[i][j] != 0:
    #             if j > avgY:
    #                 lowerArray = lowerArray + 1
    #
    # print("avgY boundary")
    # print(avgY)
    #
    # print("upper array value")
    # print(upperArray)
    # print("lower array value")
    # print(lowerArray)


    # cv2.circle(mask, (avgX, avgY), 8, (255,0,0), -1)  # make dot and put it on the average of all the positive pixels
    cv2.line(mask, (avgX-100, avgY), (avgX+100, avgY), (255, 0, 0), 8)  # make line put it on the y average


    cv2.imshow("mask", mask)  # displays mask for testing
    cv2.imshow("center", frame)  # show the normal feed with dot on top

    if avgX == 1:  # for when the light in not in frame
        print("No Light detected")
        waitTothrow = 0
    elif avgX <= 315:  # for when the light is on the left side of the frame
        print("turning Left")
        waitTothrow = 0
    elif avgX >= 335:  # for when the light is on the right side of the frame
        print("turning Right")
        waitTothrow = 0
    else:  # for when the light is in the middle of the frame
        print("its in the middle")
        waitTothrow = waitTothrow + 1

    # if M["m01"] > 2000000000:  # using the amount of pixels in the mask we can estimate the distance
    #     print("the target is really close")
    #     print("///")
    # elif M["m01"] > 100000000:
    #     print("the target is kinda close")
    #     print("////////")
    # elif M["m01"] > 50000000:
    #     print("the target is kinda far")
    #     print("///////////////")
    # else:
    #     print("the targer is really far")
    #     print("/////////////////////////")

    if waitTothrow == 10:  # if the light has been in the middle of the frame then throw the ball
        print("Throw the ball!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        waitTothrow = 0
        # break                                             # stop runing if the ball has been thrown

    if cv2.waitKey(1) & 0xff == ord('q'):  # exit if q is pressed
        break