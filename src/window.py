from tkinter import *
from tkinter import ttk
class Window():
     def __init__(self, w:int, h:int, root: Tk) -> None:
          self.width = w
          self.height = h
          self.selectedNum = 0
          self.selectedNumDisplay = StringVar(value="0")
          root.title = "Sudoku Solver"
          #root.geometry(f"{w}x{h}")
          self.mainFrame = ttk.Frame(root, padding="4 4 4 4")
          self.mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
          self.mainFrame["relief"] = "sunken"
          root.columnconfigure(0, weight=1)
          root.rowconfigure(0, weight=1)
          self.setupCanvas()
          self.setupOptions()
     def setupCanvas(self) -> None:
          self.canvas = Canvas(self.mainFrame, width=self.width, height=self.height)
          self.canvas.grid(column=0, row=0)
     def setupOptions(self) -> None:
          self.optionsFrame = ttk.Frame(self.mainFrame, padding="4 4 4 4")
          self.optionsFrame.grid(column=0,row=1, sticky=(N,W))
          self.numsFrame = ttk.Frame(self.optionsFrame, padding="1 1 1 1")
          self.numsFrame.grid(column=0,row=0, sticky= (N,W))
          self.numLabel = ttk.Label(self.optionsFrame, textvariable=self.selectedNumDisplay)
          self.numLabel.grid(column=1,row=0)
          # tried to use a loop to create button, callback would always return 9
          ttk.Button(self.numsFrame, text=f"{1}",command=lambda: self.setNum(1)).grid(column=0,row=0)
          ttk.Button(self.numsFrame, text=f"{2}",command=lambda: self.setNum(2)).grid(column=1,row=0)
          ttk.Button(self.numsFrame, text=f"{3}",command=lambda: self.setNum(3)).grid(column=2,row=0)
          ttk.Button(self.numsFrame, text=f"{4}",command=lambda: self.setNum(4)).grid(column=0,row=1)
          ttk.Button(self.numsFrame, text=f"{5}",command=lambda: self.setNum(5)).grid(column=1,row=1)
          ttk.Button(self.numsFrame, text=f"{6}",command=lambda: self.setNum(6)).grid(column=2,row=1)
          ttk.Button(self.numsFrame, text=f"{7}",command=lambda: self.setNum(7)).grid(column=0,row=2)
          ttk.Button(self.numsFrame, text=f"{8}",command=lambda: self.setNum(8)).grid(column=1,row=2)
          ttk.Button(self.numsFrame, text=f"{9}",command=lambda: self.setNum(9)).grid(column=2,row=2)
     def setNum(self, num:int) -> None:
          self.selectedNum = num
          self.selectedNumDisplay.set(f"{num}")



     #make canvas a fixed size, put it in frame, put number selection, buttons for algorithms and solve button in frame
     #pressing number button sets a variable in window to the num
     # need to figure out how to render numbers, can use canvas wrapper class to handle events, event has x,y, use that to determine what square it's in and render a number there with canvas.create_text