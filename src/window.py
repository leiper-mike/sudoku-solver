from tkinter import *
from tkinter import ttk
from board import Board
class Window():
     def __init__(self, root: Tk) -> None:
          self.selectedNumDisplay = StringVar(value="Selected: 1")
          root.title = "Sudoku Solver"
          self.mainFrame = ttk.Frame(root, padding="4 4 4 4")
          self.mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
          self.mainFrame["relief"] = "sunken"
          root.columnconfigure(0, weight=1)
          root.rowconfigure(0, weight=1)
          self.setupBoard()
          self.setupOptions()
     def setupBoard(self) -> None:
          self.canvasFrame = ttk.Frame(self.mainFrame, padding="2 2 2 2")
          self.canvasFrame.grid(column=0,row=0)
          self.board = Board(self.canvasFrame, width=300, height=300)
          self.board.grid(column=0, row=0)
          self.board.setupAndDrawCells()
     def setupOptions(self) -> None:
          self.optionsFrame = ttk.Frame(self.mainFrame, padding="4 4 4 4")
          self.optionsFrame.grid(column=0,row=1, sticky=(N,W))
          self.numsFrame = ttk.Frame(self.optionsFrame, padding="1 1 1 1")
          self.numsFrame.grid(column=0,row=0, sticky= (N,W))
          self.numLabel = ttk.Label(self.optionsFrame, textvariable=self.selectedNumDisplay)
          self.numLabel.grid(column=1,row=0, sticky=(N))
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
          ttk.Button(self.numsFrame, text=f"x",command=lambda: self.setNum(-1)).grid(column=1,row=3)
     def setNum(self, num:int) -> None:
          self.board.num = num
          if num == -1:
               self.selectedNumDisplay.set(f"Selected: Delete")
          else:
               self.selectedNumDisplay.set(f"Selected: {num}")
          



     #make canvas a fixed size, put it in frame, put number selection, buttons for algorithms and solve button in frame
     #pressing number button sets a variable in window to the num
     # need to figure out how to render numbers, can use canvas wrapper class to handle events, event has x,y, use that to determine what square it's in and render a number there with canvas.create_text