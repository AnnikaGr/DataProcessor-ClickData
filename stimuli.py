import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import ImageTk
from PIL import Image as PilImage

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))
counter =0
save_x = 0
save_y = 0

def defineAreasForStimulus(trialname, root):
    root.deiconify()

    # setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E + W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N + S)
    canvas = Canvas(frame, width=1366, height=768, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH, expand=1)

    # adding the image
    path = filedialog.askopenfilename()
    img = ImageTk.PhotoImage(PilImage.open(path))
    # prevent img from being garbage collected
    root.img = img

    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    # adding switch buttons

    switch_variable = tk.StringVar(value="area1")
    area1_button = tk.Radiobutton(root, text="area 1", variable=switch_variable,
                                indicatoron=False, value="area1", width=8)
    area2_button = tk.Radiobutton(root, text="area 2", variable=switch_variable,
                                indicatoron=False, value="area2", width=8)
    area1_button.pack(side="left")
    area2_button.pack(side="left")

    # marking stimulus areas
    stimulus = Stimulus(trialname)

    # function to be called when mouse is clicked TODO change to saving coords via stimulus.add_to_area1/2
    def savecoords(event):
        # outputting x and y coords to console
        cx, cy = event2canvas(event, canvas)
        print("(%d, %d) / (%d, %d)" % (event.x, event.y, cx, cy))
        # saving x and y coords of canvas
        global save_x
        global save_y
        global counter
        if counter % 2 == 0:
            save_x= cx
            save_y= cy
            counter += 1
        elif counter%2 != 0:
            if switch_variable.get() == "area1":
                stimulus.add_to_area1(save_x,save_y,cx,cy)
            elif switch_variable.get() == "area2":
                stimulus.add_to_area2(save_x,save_y,cx,cy)
            else:
                raise ValueError('error in switch button state - neither area1 nor area2 is selected')
            counter += 1
        else:
            raise ValueError('counting error in savecoords function')

    # mouseclick event
    canvas.bind("<ButtonPress-1>", savecoords)
    canvas.bind("<ButtonRelease-1>", savecoords)

    # wait for input of clicks
    var = tk.IntVar()
    button = tk.Button(root, text="Continue", command=lambda: var.set(1))
    # button.place(relx=.5, rely=.5, anchor="c")
    button.pack(side=tk.RIGHT, anchor=tk.SE)

    print("waiting...")
    button.wait_variable(var)
    print("done waiting.")

    # destroy widgets
    frame.destroy()
    button.destroy()
    area1_button.destroy()
    area2_button.destroy()

    #TODO save stimulus information
    return stimulus


def restoreAreasForStimulus(trialname):
    # TODO restore from file and return Stimulus class (evaluates to true??)

    return False


class Stimulus:

    def __init__(self, trialname):
        # TODO check if you are supposed to do that
        self.stimulus_object = self;
        self.trialname = trialname
        self.areas_type1 = []
        self.areas_type2 = []

    def add_to_area1(self, x1, y1, x2, y2):
        rectangle = Rectangle(x1,y1,x2,y2)
        self.areas_type1.append(rectangle)

    def add_to_area2(self, x1, y1, x2, y2):
        rectangle = Rectangle(x1,y1,x2,y2)
        self.areas_type2.append(rectangle)

class Rectangle:
    def __init__(self, x1,y1,x2,y2):
        #set left and right boundaries
        if (x1<x2):
            self.left_boundary= int(round(x1))
            self.right_boundary= int(round(x2))
        elif (x2<x1):
            self.left_boundary= int(round(x2))
            self.right_boundary= int(round(x1))
        else:
            raise ValueError('Specified rectangle has size of 0 (x1==x2)')

        #set top and bottom boundaries
        if (y1<y2):
            self.bottom_boundary= int(round(y1))
            self.top_boundary= int(round(y2))
        elif (y2<y1):
            self.bottom_boundary= int(round(y2))
            self.top_boundary= int(round(y1))
        else:
            raise ValueError('Specified rectangle has size of 0 (y1==y2)')
