import time, sys
import ps_drone
import cv2
import numpy.f2py

drone = ps_drone.Drone()
drone.startup()
drone.reset()

while (drone.getBattery()[0] == -1):
    time.sleep(0.1)

    ##print("Battery: ",str(drone.getBattery()[0], " %   ",str(drone.getBattery()[1])))

    drone.useDemoMode(True)

    ######Main

    drone.setConfigA11ID()
drone.sdVideo()
drone.frontCam()
CDC = drone.ConfigDataCount

while CDC == drone.ConfigDataCount:
    time.sleep(0.0001)

drone.takeoff()
time.sleep(7.5)
drone.moveUp(0.8)
time.sleep(2)
drone.stop()
drone.setSpeed(0.5)

stop = False

while not stop:
    while drone.VideoImageCount == IMC:
        time.sleep(0.01)
        IMC = drone.VideoImageCount
        key = drone.getkey()
    if key:
        stop = True
        img = drone.VideoImage
        gray = cv2.cvtColor(img, cv2.Color_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        circles = cv2.HougCircles(gray, cv2.Hough_GRADIENT, 0, 01, 250, minRadius=20, maxRadius=500)

        if circles != None:
            print
            "Circle here"
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # the outer circle
                cv2.circle(gray, (i[0], i[1], i[2], (0, 255, 0), 2))
                # center for the circle
                cv2.circle(gray, (i[0], i[1], 2, (0, 0, 255), 3))
                x = i[0]
                y = i[1]
                if y > 0 and y < 170:
                    print
                    "Going up"
                    drone.moveUp(0.02)
                    time.sleep(1)
                    drone.stop()
                elif x > 360 and x < 660:
                    print
                    "Move Right"
                    drone.moveRight(0.05)
                    time.sleep(1)
                    drone.stop()
                elif y > 200 and y < 360:
                    print
                    "Going down"
                    drone.moveDown(0.02)
                    time.sleep(1)
                    drone.stop()
                elif x > 0 and x < 280:
                    print
                    "Move Left "
                    drone.moveLeft(0.05)
                    time.sleep(1)
                    drone.stop()
                elif x > 280 and x < 360 and y > 160 and y < 200:
                    print
                    "Move Forward"
                    drone.moveForward(0.3)
                    time.sleep(2)
                    drone.stop()

                    #  cv2.imshow('Dronens video',gray)
        cv2.waitKey(1)
        drone.land()





