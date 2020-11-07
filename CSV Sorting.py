import csv
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from tkinter import *
import os

# Default values
input_csv = ''
output_csv = 'sorted.csv'
default_output_csv = 'sorted.csv'
header_colunm = 1


# Working with CSV files
def load_file():
    global input_csv, output_csv
    dir_name = os.getcwd()
    input_csv = askopenfilename(initialdir=dir_name, title="Select file", filetypes=(("CSV file", ".csv"), ("all files", "*.*")))
    inp_csv.delete(0, END)
    inp_csv.insert(0, input_csv.split('/')[-1])
    output_csv = out_csv.get()
    if output_csv == '' or output_csv == default_output_csv:
        output_csv = input_csv.split('.csv')[0] + '_sorted.csv'
        out_csv.delete(0, END)
        out_csv.insert(0, output_csv)


def select_output_file():
    global output_csv
    dir_name = os.getcwd()
    output_csv = asksaveasfilename(initialdir=dir_name, title="Select file", filetypes=(("CSV file", ".csv"), ("all files", "*.*")))
    if not output_csv.endswith('.csv'):
        output_csv += '.csv'
    out_csv.delete(0, END)
    out_csv.insert(0, output_csv)


def main_program():
    global output_csv, input_csv
    output_csv = out_csv.get().strip()
    if input_csv == '':
        input_csv = inp_csv.get().strip()
    if not output_csv.endswith('.csv'):
        output_csv += '.csv'
    if input_csv == '':
        load_file()
    master.destroy()

    with open(input_csv, mode='rt') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    
    if header_colunm == 1:
        data1 = data[1:]
        data1.sort()
        data[1:] = data1
    else:
        data.sort()
    
    with open(output_csv, 'w', newline='') as final:
         writer = csv.writer(final, delimiter=',')
         for row in data:
             writer.writerow(row)


def ignore_header_colunm(*args):
    global header_colunm
    header_colunm = header.get()


# ------------------ MAIN PROGRAM -----------------------------------
master = tk.Tk()
Title = master.title("Sorting CSV file")
tk.Label(master, text="Input CSV:").grid(row=0, column=0, pady=2, padx=3)
tk.Label(master, text="Output (sorted) CSV:").grid(row=1, column=0, pady=2, padx=3)

inp_csv = tk.Entry(master, width=50)
inp_csv.insert(END, input_csv)
inp_csv.grid(row=0, column=1, padx=0, sticky=W)

out_csv = tk.Entry(master, width=50)
out_csv.insert(END, output_csv)
out_csv.grid(row=1, column=1, padx=0, sticky=W)

tk.Button(master, text='Browse', command=load_file, width=15).grid(row=0, column=2, pady=3, padx=8)
tk.Button(master, text='Browse', command=select_output_file, width=15).grid(row=1, column=2, pady=3, padx=8)

tk.Label(master, text="________________________________________________________________________________________________").grid(row=2, columnspan=3)

header = IntVar(value=header_colunm)
Checkbutton(master, text="Ignore Header row (header will not be sorted)", font=("Helvetica", 9, "italic"), variable=header).grid(row=3, sticky=W, padx=20, columnspan=3, pady=0)
header.trace('w', ignore_header_colunm)

tk.Button(master, text='Quit', font=("Helvetica", 9, "bold"), command=master.quit, width=20, heigh=2).grid(row=4, column=0, pady=5, padx=60, columnspan=2, sticky=W)
tk.Button(master, text='Save Sorted CSV', font=("Helvetica", 9, "bold"), state='active', command=main_program, width=20, heigh=2).grid(row=4, column=1, pady=10, padx=60, columnspan=2, sticky=E)

tk.mainloop()
