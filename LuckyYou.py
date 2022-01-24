import threading
import random
import datetime
from time import sleep

import numpy as np
import cv2 as cv
from PIL import Image, ImageTk

from tkinter import Tk, Frame, Button, BOTH, Label
from tkinter import font as tkFont
from playsound import playsound

bg_white = np.ones((300, 300, 3), dtype=np.uint8) * 255        
# load profile photos
photoAll = cv.imread('./Photos.jpg')
single_photo_size = 300
# N = (photoAll.shape[0] // 300) * (photoAll.shape[1] // 300)
# Read roster file, program quits if not exists
with open("./Roster.txt", "r") as f:
    roster = f.readlines()
N = sum(1 for line in open('./Roster.txt'))   # count # of students
try:
    record_f = open("./Record.txt", "r")      # Check if record exists
except:
    i = 0;
    record_f = open("./Record.txt", "a")
    for student_name in roster:                 # Creates a default record file 
        lastname, firstname, netID = roster[i].split(', ')[:3]
        txt = str(i+1) + ' ' + '1' + ' ' + '0' + ' ' + '0' + ' ' + lastname + ' ' + firstname + '\n'
        record_f.write(txt)            
        i = i+1;
    record_f.close()
    record_f = open("./Record.txt", "r")      # Check if record exists
    
record = record_f.readlines() 
record_f.close()

def retrievePerson(idx, src=photoAll, unit=single_photo_size, r=roster):
    originaltxt = record[idx]
    num, status, select, accum, lastname, firstname = originaltxt.split()
    if lastname == 'A':
        return bg_white, 'Unknown', originaltxt

    top = (idx // 4) * unit
    left = (idx % 4) * unit
    fullname = firstname + ' ' + lastname    
    return src[top:top+unit, left:left+unit], fullname, originaltxt

def cvMat2tkImg(arr):
    rgb = cv.cvtColor(arr, cv.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    return ImageTk.PhotoImage(img)

class App(Frame):
    def __init__(self, winname='LuckyYou'):
        self.root = Tk()
        global helv18
        helv18 = tkFont.Font(family='Helvetica', size=18, weight='bold')
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        # print("Width",windowWidth,"Height",windowHeight)
        self.root.wm_title(winname)
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight, positionDown))        
        self.root.wm_protocol("WM_DELETE_WINDOW", self.exitApp)
        
        Frame.__init__(self, self.root)
        self.pack(fill=BOTH, expand=1)

        self.stopflag = True
        image = cvMat2tkImg(bg_white)
        self.fullname = 'Unknown'
        self.originaltxt = None

        self.panel = Label(image=image)
        self.panel.image = image
        self.panel.pack(side="top")
        self.text = Label(text=self.fullname, font=helv18)
        self.text.pack(side="top")

        # buttons
        btnClear = Button(text="Clear", command=self.clearmode)
        btnClear['font'] = helv18
        btnClear.pack(side='left')
        
        btnRecord = Button(text="Record", command=self.add2record)
        btnRecord['font'] = helv18
        btnRecord.pack(side='left')
        
        global btnRun
        btnRun = Button(text='Start', command=self.switchmode)
        btnRun['font'] = helv18
        btnRun.pack(side='right')

        # threading
        self.stopevent = threading.Event()
        self.thread = threading.Thread(target=self.spin, args=())
        self.thread.start()

    def spin(self):
        while not self.stopevent.is_set():
            if not self.stopflag:
                global student_ID
                student_ID = random.randint(0, N-1)
                num, status, select, accum, lastname, firstname = record[student_ID].split()
                if status == '0' or select == '1': continue
                photo, name, txt = retrievePerson(student_ID)

                image = cvMat2tkImg(photo)
                self.panel.configure(image=image)
                self.panel.image = image
                self.fullname = name
                self.originaltxt = txt
                self.text.configure(text=self.fullname)
                playsound('Ding.wav', False)
                sleep(0.1)

    def add2record(self):
        if self.stopflag:
            if self.fullname != 'Unknown':
                num, status, select, accum, lastname, firstname = record[student_ID].split()
                record[student_ID] = num + ' ' + status + ' ' + '1' + ' ' + str(int(accum)+1) + ' ' + lastname + ' ' + firstname + '\n'
                with open('Record.txt', 'w') as f:
                    f.writelines(record)
                    f.close()
                self.text.configure(text='Recorded')
                
    def clearmode(self):
        for idx, line in enumerate(record):
            num, status, select, accum, lastname, firstname = line.split()
            record[idx] = num + ' ' + status + ' ' + '0' + ' ' + accum + ' ' + lastname + ' ' + firstname + '\n'
            with open('Record.txt', 'w') as f:
                f.writelines(record)
                f.close()
            self.text.configure(text='Cleared')

    def switchmode(self):
        if btnRun.config('text')[-1] == 'Start':
            btnRun.config(text='Stop')
        else:
            btnRun.config(text='Start')
        self.stopflag = not self.stopflag
                
    def run(self):
        self.root.mainloop()

    def exitApp(self):          #exit loop
        self.stopflag = True
        t = threading.Timer(0.5, self.stop)  # start a timer (non-blocking) to give main thread time to stop
        t.start()

    def stop(self):
        self.stopevent.set()
        self.root.quit()

app = App()
app.run()
