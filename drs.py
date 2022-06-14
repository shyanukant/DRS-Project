# Decision Review System by Shyanukant Rathi
# import modules
#import partial for passing argument in command in button
import tkinter 
import PIL.Image, PIL.ImageTk
import cv2
from functools import partial
import threading
import time

SET_HEIGHT = 480
SET_HEIGHT2 = 600
SET_WIDTH = 720
delay = 1
# video clip capture
stream = cv2.VideoCapture('file/demo.mp4')
# Button Action
def button(Text, Command, fgColor, bgColor, xAxis, yAxis):
    btn = tkinter.Button(
                    window, text=Text,
                    width=10, 
                    command=Command, 
                    cursor='hand2',
                    font=('Times', 14, 'bold'), 
                    fg= fgColor,
                    bg= bgColor
        )
    # btn.pack(side=tkinter.LEFT)
    btn.place(relx= xAxis, rely=yAxis)

# see pending and decision image in canvas frame
def frameView(item_frame):
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(item_frame))
    canvas.image = frame
    canvas.create_image(0,0, image = frame, anchor = tkinter.NW)

# play full clip
def playAll():
    video = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, video)
    grabbed,video = stream.read()
    frame = cv2.resize(video, (SET_WIDTH, SET_HEIGHT))
    if grabbed:
        frameView(frame)
    window.after(delay, playAll)

# check, take decision fuction
def play(speed):
    # merge video clip with speed 
    video = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, video + speed)

    _,video = stream.read()
    frame = cv2.resize(video, (SET_WIDTH, SET_HEIGHT))
    frameView(frame)

# show pending image and pass decision 
def pending(decision):
    image = 'file/pending.png'
    img_frame = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
    frameView(img_frame)
    
    time.sleep(1.5)

    if decision == 'Out':
        decision_img = 'file/out.png'
    else:
        decision_img = 'file/not_out.png'
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frameView(frame)

def out():
    thread = threading.Thread(target=pending, args=('Out',))
    thread.daemon = 1
    thread.start()
    print('you are out')

def not_out():
    thread = threading.Thread(target=pending, args=('Not Out',))
    thread.daemon = 1
    thread.start()
    print('you are not out')

# Create GUI window 
window = tkinter.Tk()
window.title("Decision Review Systme")

cv_image = cv2.cvtColor(cv2.imread('file/home.png'), cv2.COLOR_BGR2RGB)

# image processing using pilllow 
photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(cv_image))
# create canvas
canvas = tkinter.Canvas(window, height=SET_HEIGHT2, width=SET_WIDTH)
canvas.create_image(0,0, image = photo, anchor= tkinter.NW)
canvas.pack()

# Create buttons
# btn = button(text-label, button action, foreground Color, background Color, x offset = xAxis, y offset = yAxis)
btn1 = button('<< Previous', partial(play, -25), 'orange', 'black', 0.18, 0.8)
btn2 = button('< Previous',partial(play, -2), 'orange', 'black', 0.35, 0.8)
btn3 = button('Next >', partial(play, 2), 'lightgreen', 'black', 0.51, 0.8)
btn4 = button('Next >>',partial(play, 25), 'lightgreen', 'black', 0.68, 0.8)
btn5 = button('Play',playAll,'blue', 'cyan', 0.3, 0.88)
btn6 = button('Out',out, 'red', 'cyan', 0.45, 0.88)
btn8 = button('Not Out',not_out, 'darkgreen', 'cyan', 0.6, 0.88)

window.mainloop()