# Drew Simmons
# 10/30/21
# Main_pb

import cv2
import numpy as np

capture = cv2.VideoCapture(2)  # select camera that the program will uses

waitTothrow = 0

while True:
    isTrue, frame = capture.read()
    lower_ir = np.array([250, 250, 250])  # setting the high and low BGR (not RGB) values
    upper_ir = np.array([255, 255, 255])

    mask = cv2.inRange(frame, lower_ir, upper_ir)  # creates mask
    kernel = np.ones((3, 3), np.uint8)  # creates 3x3 square kernel for morphology
    mask = cv2.erode(mask, kernel, iterations=1)  # erodes mask with 3x3 square
    mask = cv2.dilate(mask, kernel, iterations=1)  # dilates mask with 3x3 square

    cv2.imshow("mask", mask)  # displayes mask for testing

    M = cv2.moments(mask)
    if M["m00"] > 0:  # if there is ir light in the frame take the average
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:  # if there is not ir light in the frame don't (dividing by 0 is bad)
        cX = 1
        cY = 1

    cv2.circle(frame, (cX, cY), 8, (255, 0, 255), -1)  # make dot and put it on the avreage of all the positive pixels
    cv2.imshow("center", frame)  # show the normal feed with dot on top

    if cX == 1:  # for when the light in not in frame
        print("No Light detected")
        waitTothrow = 0
    elif cX <= 315:  # for when the light is on the right side of the frame
        print("turning Left")
        waitTothrow = 0
    elif cX >= 335:  # for when the light is on the right side of the frame
        print("turning Right")
        waitTothrow = 0
    else:  # for when the light is in the middle of the frame
        print("its in the middle")
        waitTothrow = waitTothrow + 1

    if M["m01"] > 2000000000:  # using the amount of pixels in the mask we can estimate the distance
        print("the target is really close")
        print("///")
    elif M["m01"] > 100000000:
        print("the target is kinda close")
        print("////////")
    elif M["m01"] > 50000000:
        print("the target is kinda far")
        print("///////////////")
    else:
        print("the targer is really far")
        print("/////////////////////////")

    if waitTothrow == 10:  # if the light has been in the middle of the frame then throw the ball
        print("Throw the ball!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        waitTothrow = 0
        # break                                             # stop runing if the ball has been thrown

    if cv2.waitKey(1) & 0xff == ord('q'):  # exit if q is pressed
        break