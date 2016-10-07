import numpy as n
import cv2 as cv
import time

def PrintCamInfo(capture):
    w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv.CAP_PROP_FPS)
    print("Frames width : {0}".format(w))
    print("Frames height : {0}".format(h))
    print("fps : {0}".format(fps))
    return (w,h, fps)
    
capture = None
found = -1
devices = []
viewer = []

def add_device(capture, devices):
    if capture and capture.isOpened:
        ret, frame = capture.read()
        if ret != False:
            devices.append(capture)
            print("Detecing camera {0}".format(len(devices)-1))
            return True
    return False

for i in range(2):
    capture = cv.VideoCapture(i)
    if add_device(capture, devices) == False:
        capture = None    

print(len(devices))

capture = None
device_id = 0
if len(devices) > 1:
    response = input("Please enter the device you wish to connect: ")
    device_id = int(response)
    capture = devices[device_id]  
elif len(devices) == 1:
    capture = devices[0]  

previous_frame = None
show_diff = False
if capture is not None:

    (w,h,fps) = PrintCamInfo(capture)
    frame_duration_ms = 1
    
    viewer.append('Camera ' + str(found) + ' image size : ' + str(w) + 'x' + str(h))
    while(True):
        now = time.time() * 1000
        ret, frame = capture.read()
        display = frame
        if ret != False:
            cv.imshow(viewer[0], display)
            previous_frame = n.copy(frame)
        duration = time.time() * 1000 - now

        wait_time = 1

        k = cv.waitKey(wait_time)

        if k == ord('q') or k == 27:
            break
        if k == ord('d'):
            show_diff = not show_diff
        if k == 32:
            frame_by_frame = not frame_by_frame
    



