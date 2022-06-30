# Decision Review System by Shyanukant Rathi
# import modules
#import partial for passing argument in command in button
import tkinter 
from tkinter import  filedialog
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import time
import cv2

SET_HEIGHT = 480
SET_WIDTH = 720
delay = 1
# video clip capture
# Upload Your Video
def uploadFile():
    file = filedialog.askopenfilename(filetypes=[("Video", '.MP4'),("All file, '*.*")])
    uploadVideo(file)
    # want to change file
    btn1.config(command=uploadFile)
    
# Demo video
def demoVideo():
    file = 'file/demo.mp4'
    uploadVideo(file)
    # want to restart
    btn0.config(command=demoVideo)
    

def uploadVideo(filename):
    global stream, photo2
    stream = cv2.VideoCapture(f'{filename}')
    # read frame of video, convert in image and exchange with home.png
    _, video = stream.read()
    videoFrame = cv2.resize(video, (SET_WIDTH, SET_HEIGHT))
    photo2 = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(videoFrame))
    canvas.itemconfig(home_container, image = photo2)

    # after click on demo all button enable
    for btn in (btn2,btn3,btn4,btn5,btn6,btn7,btn8):
        btn.config(state='normal')

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
        
    if grabbed:
        frame = cv2.resize(video, (SET_WIDTH, SET_HEIGHT))
        frameView(frame)
        window.after(delay, playAll)
    # else:
    #     stream.release()
        
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
    for btn in (btn2,btn3,btn4,btn5,btn6,btn8):
        btn.config(state='disabled')

def not_out():
    thread = threading.Thread(target=pending, args=('Not Out',))
    thread.daemon = 1
    thread.start()
    for btn in (btn2,btn3,btn4,btn5,btn6,btn7):
        btn.config(state='disabled')
         
# Create GUI window ################################################################
if __name__ == '__main__':

    Font = ('Times', 14, 'bold')
    window = tkinter.Tk()
    window.title("Decision Review System")
    photo = tkinter.PhotoImage(file='file/home.png')
    # create canvas
    canvas = tkinter.Canvas(window, height=SET_HEIGHT, width=SET_WIDTH)
    home_container = canvas.create_image(0,0, image = photo, anchor= tkinter.NW)
    canvas.pack()

    # Create buttons into frames
    # btn = button(text-label, button action, foreground Color, background Color,)
    frame1 = tkinter.Frame(window)
    frame1.pack(pady=10)
    btn0 = tkinter.Button(frame1, text='Demo', command=demoVideo, font=Font, width=10, fg='black', bg='red')
    btn0.pack(side=tkinter.LEFT)
    btn1 = tkinter.Button(frame1, text='Upload',command=uploadFile, font=Font, width=10, fg='black', bg='red')
    btn1.pack(side=tkinter.LEFT)

    frame2 = tkinter.Frame(window)
    frame2.pack(pady=10)
    btn2 = tkinter.Button(frame2, text='<< Previous', command= partial(play, -25), font=Font, width=10, fg='orange', bg='black', state='disabled')
    btn2.pack(side=tkinter.LEFT)
    btn3 = tkinter.Button(frame2, text='< Previous', command= partial(play, -2), font=Font, width=10, fg='orange', bg='black', state= 'disabled')
    btn3.pack(side=tkinter.LEFT)
    btn4 = tkinter.Button(frame2, text='Forward >', command= partial(play, 2), font=Font, width=10, fg= 'lightgreen', bg='black', state='disabled')
    btn4.pack(side=tkinter.LEFT)
    btn5 = tkinter.Button(frame2, text= 'Forward >>', command= partial(play, 25),font=Font, width=10, fg= 'lightgreen', bg='black', state='disabled')
    btn5.pack(side=tkinter.LEFT)

    frame3 = tkinter.Frame(window)
    frame3.pack(pady=10)
    btn6 = tkinter.Button(frame3, text= 'Play', command= playAll, font=Font, width=10, fg='blue', bg='cyan' , state='disabled')
    btn6.pack(side=tkinter.LEFT)
    btn7 = tkinter.Button(frame3, text= 'Out', command= out, font=Font, width=10, fg= 'red', bg= 'cyan', state='disabled')
    btn7.pack(side=tkinter.LEFT)
    btn8 = tkinter.Button(frame3, text= 'Not Out', command= not_out, font=Font, width=10, fg= 'darkgreen', bg= 'cyan', state='disabled')
    btn8.pack(side=tkinter.LEFT)

    # bind one more event into button
    window.mainloop()