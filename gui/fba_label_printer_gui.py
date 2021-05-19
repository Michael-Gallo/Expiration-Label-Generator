#FBA Label Printer.py  -   Create 5160 labels that match dates and quantities given by the user with a UI

import tkinter
import os
import datetime 
import subprocess
import logging
try:
    import win32print
    import win32api
except:
    pass
from tkinter import *
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import babel  #Babel imports necessary for pyinstaller to recognize babel, not necessary for script to run
import babel.numbers
from labelwriter import createAvery5160Spec, write_date , save_from_tuples

logging.basicConfig(level = logging.DEBUG, format = '%(message)s')
global icon
icon="printer.png"
root = Tk()
root.title("FBA Label Printer")





def printOut(name="printTemp.pdf"): #save the current UI to a file, print, and delete the file
    save(name)
    if printBoxBool==False:
        save(name)
        os.startfile(name,'print')
    else:
        createPrintWindow(name)
def openPDF(name="labels.pdf"):
    save(name)
    subprocess.Popen(name,shell=True)
        

#Create UI for functions


maxrow=IntVar()
printBoxBool=BooleanVar()
printBoxBool.set(True) #Show the print dialogue by default

def addBase(): # adds the base of the UI with a set number of entry rows
##    topFrame=Frame(root)
##    topFrame.grid(side=TOP)


    maxrow.set(0)
    for i in range(5):
        addItemRow()
    addButtons(5)
def addButtons(col):
    buttonWidth=15
    topRow=1
    Button(root,text="More",command=addItemRow,width=buttonWidth).grid(row=topRow,column=col)
    Button(root,text="Save",command=save,width=buttonWidth).grid(row=topRow+1,column=col)
    Checkbutton(root,text="Print Dialogue?",variable=printBoxBool).grid(row=topRow+3,column=col)
    Button(root,text="Print",command=printOut,width=buttonWidth).grid(row=topRow+4,column=col)
    Button(root,text="Open", command=openPDF,width=buttonWidth).grid(row=topRow+2,column=col)
#Input Validation for buttons confirms there is less than 10,000 labels
def isPosInt(val):
    try:
        if int(val)>=0 and int(val)<10000:
            return True
    except ValueError:
        if val=='':
            return True
        else:
            return False
    return False
def addItemRow():  #Creates a full Item Entry Row
    maxrow.set(maxrow.get()+1)
    dateLabel= Label(root,text="Date")
    dateLabel.grid(row=maxrow.get(),column=1)
    dateEnt= DateEntry()
    dateEnt.grid(row=maxrow.get(),column=2)
    quantLabel= Label(root,text="Quantity")
    quantLabel.grid(row=maxrow.get(),column=3)
    quantEnt=Entry(root,validate="key",validatecommand=(validation,'%P'))
    quantEnt.insert(0,'0')
    quantEnt.grid(row=maxrow.get(),column=4)
    dateBoxes.append(dateEnt)
    quantBoxes.append(quantEnt)

#Create UI For printing window
def createPrintWindow(file):
    printWindow = Toplevel(root)
    setIcon(icon,printWindow) 
    printerList= getPrinterList()
    selectedPrinter=StringVar(printWindow,printerList[0])
    Label(printWindow,text="Printer:").grid(row=0,column=0)
    printerSelector = OptionMenu(printWindow,selectedPrinter,*printerList)
    printerSelector.grid(row=0,column=1)
    Label(printWindow,text="Copies:").grid(row=1,column=0)
    copies = Entry(printWindow,validate="key",validatecommand=(validation,'%P'))
    copies.insert(0,'1')
    copies.grid(row=1,column=1)
    #Button(printWindow,text="Debug",command=lambda:logging.debug(selectedPrinter.get())).grid(row=2,column=1)
    Button(printWindow,text="Print",command=lambda:printWindowPrint(file,selectedPrinter.get(),int(copies.get()))).grid(row=2,column=1)
    
def getPrinterList():
    printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL|win32print.PRINTER_ENUM_CONNECTIONS)
    printer_names= [name for (flags,description, name, comment) in printer_info]
    return(printer_names)
def printWindowPrint(file,printer,copies):
    for i in range(copies):
        win32api.ShellExecute(
        0,
        "printto",
        file,
        '"%s"' %printer,
        ".",
        0
        )

#Pyinstaller functionality

def setIcon(imageFile,windowName):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    path= os.path.join(base_path,imageFile)
    windowName.tk.call('wm','iconphoto',windowName._w,tk.PhotoImage(file=path))                       
setIcon(icon,root)    
dateBoxes=[]
quantBoxes=[]
validation = root.register(isPosInt)    
addBase()
root.mainloop()


def main():
	pass

if __name__ == '__main__':
	main()