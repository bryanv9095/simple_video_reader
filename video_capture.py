import numpy as n
import cv2 as cv
import time
import sys
import getopt
import os
from pathlib import Path

def PrintCamInfo(capture):
    w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv.CAP_PROP_FPS)
    print("Frames width : {0}".format(w))
    print("Frames height : {0}".format(h))
    print("Frames height : {0}".format(fps))
    return (w,h, fps)

def play_it(capture, full_filename):
    viewer = []
    (w,h,fps) = PrintCamInfo(capture)
    frame_duration_ms = int(1000.0/fps)
    viewer = [('Camera : image size : ' + str(w) + 'x' + str(h))]
    paused = False
    previous_frame = None
    current_frame = None
    show_diff = False
   
    ret = None
    toggle = False
    frame_id = -1
    while(True):
        now = time.time() * 1000

        if toggle is True:
            previous_frame, current_frame = current_frame, previous_frame 
        else:
            if current_frame is not None:
                previous_frame = n.copy(current_frame)
            ret, current_frame = capture.read()
            frame_id = frame_id + 1

        display = current_frame
        if ret != False:
            if show_diff:
                display = n.absolute(n.subtract(current_frame, previous_frame))
            cv.imshow(viewer[0], display)
        else:
            break
        duration = time.time() * 1000 - now

        wait_time = int(frame_duration_ms-duration)
        if paused is True:
            wait_time = 0
        k = cv.waitKey(wait_time)

        if k == ord('q') or k == 27:
            break
        if k == ord('d'):
            show_diff = not show_diff
        if k == ord('s'):
            (full_dir, filename) = os.path.split(full_filename)
            filename, ext = os.path.splitext(filename)
            img_file = os.path.join(full_dir, filename + '_Frame' + str(frame_id) + '.tif' )
            print('saving ', img_file)
            cv.imwrite(img_file,current_frame)
        if k == 32:
            paused = not paused
            if paused:
                print('pause')
            else:
                print('play')
            toggle = False
        if k == 2424832:
            if toggle is False:
                print('toggle')
            toggle = True

def main(argv):
    argument = '.'
    if argv is not None:
        if len(sys.argv) > 1:
            argument = sys.argv[1]

    files = []
    extensions = ['264', 'divx', 'avi', 'mp4', '']
    if os.path.isfile(argument):
        files.append(argument)
    elif os.path.isdir(argument):
        for root, dirs, f in os.walk(argument):
            for name in f:
                ext = os.path.splitext(name)[1][1:]
                if ext in extensions:
                    files.append(os.path.join(root, name))       

    for f in files:
        capture = cv.VideoCapture(f)
        if capture and capture.isOpened:
            print('playing ', f)
            play_it(capture, f)

if __name__ == "__main__":
    main(sys.argv)


