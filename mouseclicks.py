import pandas as pd
import xlrd


# read mouseclick data from excel file for a certain trial (i.e. a certain stimulus)
def extract_mouse_clicks_from_file(filepath, sheetname, trialname):
    excel_data = pd.read_excel(filepath, sheet_name=sheetname)
    mouse_click_list = []

    for index, row in excel_data.iterrows():
        if row["screen:mainscreen"] == trialname:
            mouse_click = MouseClick(row["X Coordinate"], row["Y Coordinate"], row["Reaction Time"])
            mouse_click_list.append(mouse_click)

    return mouse_click_list


class MouseClick:

    def __init__(self, coord_x, coord_y, reaction_time):
        self.coord_x = int(round(coord_x))
        self.coord_y = int(round(coord_y))
        self.reaction_time = reaction_time
