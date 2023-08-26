from tkinter import *
from tkinter import ttk, filedialog
import datetime
from ReadHTTLog import *
import time
import pandas as pd
import glob
import os
import numpy as np

win = Tk()
win.geometry("750x350")


def get_directory():
    global directory
    directory = filedialog.askdirectory()


def get_entry():
    global treatment_time_entry
    global output_filename_entry
    global treatment_time
    global output_filename
    global pattern
    global checkbox_list
    treatment_time = treatment_time_entry.get()
    output_filename = output_filename_entry.get()
    checkbox1_value = var_maxpressure.get()
    checkbox2_value = var_spiketemp.get()
    checkbox3_value = var_laserpower.get()
    checkbox4_value = var_postmaxtemp.get()
    checkbox5_value = var_interlock.get()
    checkbox6_value = var_stable.get()
    checkbox7_value = var_initialtankpressure.get()
    checkbox8_value = var_laseron.get()
    checkbox9_value = var_laseroff.get()
    checkbox10_value = var_temprange.get()
    checkbox11_value = var_shotstart.get()
    checkbox12_value = var_shotend.get()
    checkbox13_value = var_coolingstart.get()
    checkbox14_value = var_interlockstart.get()
    checkbox15_value = var_probetype.get()
    checkbox16_value = var_pretemp.get()
    checkbox_list = [checkbox1_value, checkbox2_value, checkbox3_value, checkbox4_value, checkbox5_value, checkbox6_value,
                     checkbox7_value, checkbox8_value, checkbox9_value, checkbox10_value, checkbox11_value, checkbox12_value,
                     checkbox13_value, checkbox14_value, checkbox15_value, checkbox16_value]
    pattern = pattern_entry.get()
    if not output_filename:
        output_filename = "output" + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H")
    if not treatment_time_entry:
        treatment_time_entry = ''
    try:
        ReadHTT(directory, output_filename, treatment_time, checkbox_list, pattern)
    except NameError:
        print("Working directory not found")


# Treatment Time Field
label_treatment = Label(
    win,
    text="Treatment Time (min)",
    bg='blue',
    fg='white',
)
label_treatment.place(x=1, y=5)
treatment_time_entry = Entry(win, width=10)
treatment_time_entry.place(x=126, y=5)

# Checkboxes
label_checkbox = Label(
    win,
    text="Variables to be exported:",
    bg='blue',
    fg='white',
)
label_checkbox.place(x=1, y=35)
var_maxpressure = BooleanVar()
var_spiketemp = BooleanVar()
var_laserpower = BooleanVar()
var_postmaxtemp = BooleanVar()
var_interlock = BooleanVar()
var_stable = BooleanVar()
var_initialtankpressure = BooleanVar()
var_laseron = BooleanVar()
var_laseroff = BooleanVar()
var_temprange = BooleanVar()
var_shotstart = BooleanVar()
var_shotend = BooleanVar()
var_coolingstart = BooleanVar()
var_interlockstart = BooleanVar()
var_probetype = BooleanVar()
var_pretemp = BooleanVar()

checkbox1 = Checkbutton(win, text="MaxPressure", variable=var_maxpressure)
checkbox2 = Checkbutton(win, text="SpikeTemp", variable=var_spiketemp)
checkbox3 = Checkbutton(win, text="LaserPower", variable=var_laserpower)
checkbox4 = Checkbutton(win, text="MaxTemp", variable=var_postmaxtemp)
checkbox5 = Checkbutton(win, text="Interlock", variable=var_interlock)
checkbox6 = Checkbutton(win, text="Stable", variable=var_stable)
checkbox7 = Checkbutton(win, text="InitialTankPressure", variable=var_initialtankpressure)
checkbox8 = Checkbutton(win, text="LaserOnTime", variable=var_laseron)
checkbox9 = Checkbutton(win, text="LaserOffTime", variable=var_laseroff)
checkbox10 = Checkbutton(win, text="CoolingTempRange", variable=var_temprange)
checkbox11 = Checkbutton(win, text="ShotStartTimeStamp", variable=var_shotstart)
checkbox12 = Checkbutton(win, text="ShotEndTimeStamp", variable=var_shotend)
checkbox13 = Checkbutton(win, text="CoolingStartTimeStamp", variable=var_coolingstart)
checkbox14 = Checkbutton(win, text="InterlockStartTimeStamp", variable=var_interlockstart)
checkbox15 = Checkbutton(win, text="ProbeType", variable=var_probetype)
checkbox16 = Checkbutton(win, text="InitialTemp", variable=var_pretemp)
checkbox1.place(x=5, y=56)
checkbox2.place(x=5, y=76)
checkbox3.place(x=5, y=96)
checkbox4.place(x=5, y=116)
checkbox5.place(x=5, y=136)
checkbox6.place(x=5, y=156)
checkbox7.place(x=5, y=176)

checkbox8.place(x=300, y=56)
checkbox9.place(x=300, y=76)
checkbox10.place(x=300, y=96)
checkbox11.place(x=300, y=116)
checkbox12.place(x=300, y=136)
checkbox13.place(x=300, y=156)
checkbox14.place(x=300, y=176)

checkbox15.place(x=595, y=56)
checkbox16.place(x=595, y=76)
checkbox_list = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

# Filename Field
label_filename = Label(
    win,
    text="Export Filename (.xlsx)",
    bg='blue',
    fg='white',
)
label_filename.place(x=1, y=205)
output_filename_entry = Entry(win, width=40)
output_filename_entry.place(x=130, y=205)

# Pattern Field
label_pattern = Label(
    win,
    text="One common text in all sub-folder names",
    bg='blue',
    fg='white',
)
label_pattern.place(x=1, y=235)
pattern_entry = Entry(win, width=40)
pattern_entry.place(x=233, y=235)
Label(win, text="leave blank if using everything in the working folder", font=("Calibri", 8, "italic")).place(x=232, y=254)

ttk.Button(win, text="Set Working Directory", width=20, command=get_directory).place(x=750/2, y=200)
ttk.Button(win, text="Finish", width=10, command=get_entry).place(x=750/2, y=285)
win.mainloop()

