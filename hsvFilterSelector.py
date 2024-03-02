import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import filedialog


def empty(*args):

    pass

def filterSelector(imgPath):

    screenWidth, screenHeight = pyautogui.size()
    adjustedHeight=(screenHeight//2)+235
    adjustedWidth=screenWidth-16
    maskHeight=screenHeight//5
    maskWidth=screenWidth//5

    cv2.namedWindow("HSV Filter Selector", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("HSV Filter Selector", adjustedWidth,adjustedHeight)
    cv2.moveWindow("HSV Filter Selector",0,16)

    cv2.createTrackbar("Hue Min","HSV Filter Selector",0,179,empty)
    cv2.createTrackbar("Hue max","HSV Filter Selector",179,179,empty)
    cv2.createTrackbar("Sat Min","HSV Filter Selector",0,255,empty)
    cv2.createTrackbar("Sat Max","HSV Filter Selector",255,255,empty)
    cv2.createTrackbar("Val Min","HSV Filter Selector",0,255,empty)
    cv2.createTrackbar("Val Max","HSV Filter Selector",255,255,empty)

    cv2.namedWindow("HSV Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("HSV Mask",maskWidth ,maskHeight)
    cv2.moveWindow("HSV Mask",(adjustedWidth//2)-(maskWidth//2),adjustedHeight+48)

    while True:

        imgOri=cv2.imread(imgPath)
        imgOri=cv2.resize(imgOri,(0,0),None,.5,.5)
        imgHSV=cv2.cvtColor(imgOri,cv2.COLOR_BGR2HSV)

        hMin=cv2.getTrackbarPos("Hue Min","HSV Filter Selector")
        hMax=cv2.getTrackbarPos("Hue max","HSV Filter Selector")
        sMin=cv2.getTrackbarPos("Sat Min","HSV Filter Selector")
        sMax=cv2.getTrackbarPos("Sat Max","HSV Filter Selector")
        vMin=cv2.getTrackbarPos("Val Min","HSV Filter Selector")
        vMax=cv2.getTrackbarPos("Val Max","HSV Filter Selector")

        lower =np.array([hMin,sMin,vMin])
        upper =np.array([hMax,sMax,vMax])

        imgMask=cv2.inRange(imgHSV,lower,upper)
        imgResult=cv2.bitwise_and(imgOri,imgOri,mask=imgMask)
        imgConcat=np.concatenate((imgOri,imgResult),axis=1)
        
        cv2.imshow("HSV Mask",imgMask)
        cv2.imshow("HSV Filter Selector",imgConcat)

        keyPress = cv2.waitKey(1)

        if keyPress == 27:

            cv2.destroyAllWindows()
            break

class Application:

    def __init__(self, window, windowTitle):

        self.window = window
        self.window.title(windowTitle)

        self.btnProcess = tk.Button(window, text="Select Image", width=20, command=self.processImage)
        self.btnProcess.pack(padx=20, pady=10)

        self.btnExit = tk.Button(window, text="Exit", width=20, command=self.window.destroy)
        self.btnExit.pack(padx=20, pady=10)

        self.window.mainloop()

    def processImage(self):

        imgPath=filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if imgPath:

            filterSelector(imgPath)

root = tk.Tk()
boxWidth, boxHeight = pyautogui.size()
root.geometry(f"{boxWidth//6}x{boxHeight//10}+100+100")
app = Application(root, "HSV Filter Selector")