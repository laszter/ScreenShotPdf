import os
import pyautogui
from fpdf import FPDF

import pyWinhook
import pythoncom

from tkinter import *

positions = []
num_click = 0


def mouseClickEvent(event):
    global num_click
    global positions

    positions.append(event.Position)
    num_click = num_click + 1
    return True


def optimizePosition(pos):
    if len(pos) != 2:
        return {0, 0, 0, 0}

    x = pos[0][0]
    y = pos[0][1]
    x2 = pos[1][0]
    y2 = pos[1][1]

    w = abs(x - x2)
    h = abs(y - y2)

    if x > x2:
        x = x2

    if y > y2:
        y = y2

    return x, y, w, h


def scanscreen():
    root.wm_state('iconic')

    global num_click
    global positions

    positions = []
    num_click = 0

    fileNameValue = fileName.get()
    numPageValue = numPage.get()

    if fileNameValue == "":
        fileNameValue = "untitle"

    if numPage == 0:
        print("Invalid number of pages.")
        return

    hm = pyWinhook.HookManager()
    hm.SubscribeMouseAllButtonsDown(mouseClickEvent)
    hm.HookMouse()

    while num_click < 2:
        pythoncom.PumpWaitingMessages()

    hm.UnhookMouse()

    dir = "./images_tmp"
    if (not os.path.exists("./images_tmp")):
        os.makedirs("./images_tmp")

    x, y, w, h = optimizePosition(positions)

    for i in range(numPageValue):
        myScreenshot = pyautogui.screenshot(region=(x, y, w, h))
        myScreenshot.save(os.path.join(dir, "tmp_"+str(i)+".png"))
        pyautogui.press('right')

    pdf = FPDF()

    for file in os.scandir(dir):
        pdf.add_page()
        pdf.image(file.path, 0, 0, 210, 297)
    pdf.output(fileNameValue + ".pdf", "F")

    for file in os.scandir(dir):
        os.remove(file.path)
    os.removedirs(dir)
    print("scan complete")
    root.wm_state('normal')

def move_app(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

def exit_app(event):
    root.quit()

if __name__ == "__main__":
    root = Tk()
    root.title("Scan Screen PDF")
    root.resizable(False, False)

    # Gets the requested values of the height and widht.
    windowWidth = 300
    windowHeight = 200

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

    # Positions the window in the center of the page.
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
    root.columnconfigure(0)
    root.columnconfigure(1)

    # ----- custom title bar -------
    # root.overrideredirect(1)

    # titleBar = Frame(root, bg="blue", relief="raised",bd=0)
    # titleBar.pack(expand=0, fill=X)
    # titleBar.bind("<B1-Motion>", move_app)

    # titleLabel = Label(titleBar, text="My App", bg="blue", fg="white")
    # titleLabel.pack(side=LEFT, pady=6)

    # closeTitleBar = Label(titleBar, text="  X  ", bg="blue", fg="white", relief="raised", bd=0)
    # closeTitleBar.pack(side=RIGHT, pady=6)
    # closeTitleBar.bind("<Button-1>", exit_app)

    # File Name
    Label(root, text="File Name: ",font="32").grid(column=0,row=0,sticky=E, pady=10)

    fileName = StringVar(value="untitle")
    fileNameText = Entry(root, textvariable=fileName,font="32").grid(column=1,row=0, sticky=EW, padx=10, pady=10)

    # Number of pages
    Label(root, text="Num Page: ",font="32").grid(column=0,row=1,sticky=E, pady=20)

    numPage = IntVar(value=1)
    numPageText = Entry(root, textvariable=numPage,font="32",justify=RIGHT,width=5).grid(column=1,row=1, sticky=E, padx=10, pady=10)

    # eventNext = BooleanVar(value=False)
    # eventNextChk = Checkbutton(root, text="Right", textvariable=eventNext, font="32").grid(column=1,row=2, pady=10)
    # eventNextChk = Checkbutton(root, text="Right", textvariable=eventNext, font="32").grid(column=1,row=2, pady=10)
    # eventNextChk = Checkbutton(root, text="Right", textvariable=eventNext, font="32").grid(column=1,row=2, pady=10)

    # Scan button
    scanBtn = Button(root, text="  Scan  ",font="32", command=scanscreen).grid(column=1,row=3,sticky=E,padx=20)

    root.mainloop()
