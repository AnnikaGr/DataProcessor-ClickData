
import mouseclicks
import stimuli
import evaluate
import tkinter as tk
from tkinter import filedialog

#read mouseClicks from File

root = tk.Tk()
root.withdraw()

print("Select excel file with data")
path = filedialog.askopenfilename()

trialname=1 #TODO verwende etwas wie: input("What is the name of the relevant trial?") was aber keinen Einfluss auf filedialog hat

#parameter: path to excel file, name of relevant sheet, trialname as specified in excel colum heading
mouse_click_list = mouseclicks.extract_mouse_clicks_from_file(path, "optimalerDateninput", trialname)

#areas fuer trial festlegen oder aus Datei laden

stimulus = stimuli.restoreAreasForStimulus(trialname)

if stimulus:
    pass
else:
    stimulus = stimuli.defineAreasForStimulus(trialname, root)


# Evaluate which clicks have been placed in which area

result = evaluate.evaluatePositions(mouse_click_list, stimulus)

evaluate.displayResult(result, root)

tk.mainloop()