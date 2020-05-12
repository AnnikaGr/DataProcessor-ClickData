from PIL import ImageTk
import tkinter as tk
from PIL import Image as PilImage
from tkinter import *
from tkinter import filedialog

def evaluatePositions(mouse_click_list, stimulus):
    mouse_clicks_area1 = []
    mouse_clicks_area2 = []
    mouse_clicks_miss = []

    for mouse_click in mouse_click_list:
        appended = 0
        for rectangle in stimulus.areas_type1:
            if mouse_click.coord_x >= rectangle.left_boundary and mouse_click.coord_x <= rectangle.right_boundary and mouse_click.coord_y >= rectangle.bottom_boundary and mouse_click.coord_y <= rectangle.top_boundary:
                mouse_clicks_area1.append(mouse_click)
                appended = 1
        for rectangle in stimulus.areas_type2:
            if mouse_click.coord_x >= rectangle.left_boundary and mouse_click.coord_x <= rectangle.right_boundary and mouse_click.coord_y >= rectangle.bottom_boundary and mouse_click.coord_y <= rectangle.top_boundary:
                mouse_clicks_area2.append(mouse_click)
                appended = 1
        if appended == 0:
            mouse_clicks_miss.append(mouse_click)

    if len(mouse_click_list) > len(mouse_clicks_area1) + len(mouse_clicks_area2) + len(mouse_clicks_miss):
        raise ValueError('Some Mouseclick(s) must have been added to several lists')
    elif len(mouse_click_list) < len(mouse_clicks_area1) + len(mouse_clicks_area2) + len(mouse_clicks_miss):
        raise ValueError('Some Mouseclick(s) have not been added to any list')

    result = Result(mouse_clicks_area1, mouse_clicks_area2, mouse_clicks_miss, stimulus)
    return result

def displayResult (result, root):
    print("Trialname: " + str(result.stimulus.trialname))
    print("Select trial image: ")

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
    img = tk.PhotoImage(file = path)
    # prevent img from being garbage collected
    root.img = img

    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    for mouseclick in result.mouse_clicks_miss:
        img.put("red", to=(mouseclick.coord_x-3, mouseclick.coord_y-3, mouseclick.coord_x+3, mouseclick.coord_y+3))

    for mouseclick in result.mouse_clicks_area1:
        img.put("{#%02x%02x%02x} % (66, 135, 245)", to=(mouseclick.coord_x-3, mouseclick.coord_y-3, mouseclick.coord_x+3, mouseclick.coord_y+3))

    for mouseclick in result.mouse_clicks_area2:
         img.put("{blue}", to=(mouseclick.coord_x - 3, mouseclick.coord_y - 3, mouseclick.coord_x + 3, mouseclick.coord_y + 3))

    for rectangle in result.stimulus.areas_type1:
         img.put("{#adc9a7}", to=(rectangle.top_boundary, rectangle.left_boundary, rectangle.bottom_boundary, rectangle.right_boundary))

    for rectangle in result.stimulus.areas_type2:
         img.put("{#a7c9c8}", to=(rectangle.top_boundary, rectangle.left_boundary, rectangle.bottom_boundary, rectangle.right_boundary))



class Result:
    def __init__(self, mouse_clicks_area1, mouse_clicks_area2, mouse_clicks_miss, stimulus):
        self.mouse_clicks_area1 = mouse_clicks_area1
        self.mouse_clicks_area2 = mouse_clicks_area2
        self.mouse_clicks_miss = mouse_clicks_miss
        self.stimulus = stimulus
