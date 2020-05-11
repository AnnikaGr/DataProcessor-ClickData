from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import PIL
from PIL import ImageTk

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))


def defineAreasForStimulus(trialname):
    root = Tk()

    # setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E + W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N + S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH, expand=1)

    # adding the image
    path = filedialog.askopenfilename()
    img = ImageTk.PhotoImage(Image.open(path))
   # File = askopenfilename(parent=root, initialdir="M:/", title='Choose an image.')
    #print("opening %s" % File)
    #img = PhotoImage(file=File)

    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    stimulus = Stimulus(trialname)

    # function to be called when mouse is clicked TODO change to saving coords via stimulus.add_to_area1/2
    def printcoords(event):
        # outputting x and y coords to console
        cx, cy = event2canvas(event, canvas)
        print("(%d, %d) / (%d, %d)" % (event.x, event.y, cx, cy))

    # mouseclick event
    canvas.bind("<ButtonPress-1>", printcoords)
    canvas.bind("<ButtonRelease-1>", printcoords)

    root.mainloop()
     #TODO break loop
    #TODO save stimulus
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
            self.left_boundary=x1
            self.right_boundary=x2
        elif (x2<x1):
            self.left_boundary=x2
            self.right_boundary=x1
        else:
            raise ValueError('Specified rectangle has size of 0 (x1==x2)')

        #set top and bottom boundaries
        if (y1<y2):
            self.bottom_boundary=y1
            self.top_boundary=y2
        elif (y2<y1):
            self.bottom_boundary=y2
            self.top_boundary=y1
        else:
            raise ValueError('Specified rectangle has size of 0 (y1==y2)')
