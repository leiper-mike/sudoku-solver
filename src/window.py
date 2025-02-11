from tkinter import *
from tkinter import ttk
from src.board import Board
class Window():
     def __init__(self, root: Tk) -> None:
          self.selectedNumDisplay = StringVar(value="Selected: 1")
          self.root = root
          root.title("Sudoku Solver")
          self.mainFrame = ttk.Frame(root, padding="4 4 4 4")
          self.mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
          self.mainFrame["relief"] = "sunken"
          self.algorithm = 0
          root.columnconfigure(0, weight=1)
          root.rowconfigure(0, weight=1)
          self.setupBoard()
          self.setupOptions()
     def setupBoard(self) -> None:
          self.canvasFrame = ttk.Frame(self.mainFrame, padding="2 2 2 2")
          self.canvasFrame.grid(column=0,row=0, sticky= (W))
          self.board = Board(self.canvasFrame, width=300, height=300)
          self.board.grid(column=0, row=0)
          self.board.setupCells()
          self.board.setupSudoku()
          self.board.drawCells()
     def setupOptions(self) -> None:
          self.optionsFrame = ttk.Frame(self.mainFrame, padding="4 4 4 4")
          self.optionsFrame.grid(column=0,row=1, sticky=(N,W))
          self.optionsFrame["relief"] = "sunken"
          self.numsFrame = ttk.Frame(self.optionsFrame, padding="1 1 1 1")
          self.numsFrame.grid(column=0,row=0, sticky= (N,W))
          self.numLabel = ttk.Label(self.optionsFrame, textvariable=self.selectedNumDisplay, padding="10 10 ")
          self.numLabel.grid(column=1,row=0, sticky=(N,S))
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

          #algorithm button options
          algorithmFrame = ttk.Frame(self.optionsFrame, padding= "1 1 1 1")
          algorithmFrame.grid(column=2,row=0)
          ttk.Button(algorithmFrame, text="Naive", command=lambda: self.setAlgo(0),width= 15).grid(column = 2, row = 0,sticky=(S,W))
          ttk.Button(algorithmFrame, text="Advanced", command=lambda: self.setAlgo(1),width= 15).grid(column = 2, row = 1,sticky=(N,W))
          ttk.Button(algorithmFrame, text="Expert", command=lambda: self.setAlgo(2),width= 15).grid(column = 3, row = 0,sticky=(S,W))
          ttk.Button(algorithmFrame, text="Super Duper Expert", command=lambda: self.setAlgo(3),width= 15).grid(column = 3, row = 1,sticky=(N,W))
          ttk.Button(algorithmFrame, text="Solve!", command=lambda: self.solve()).grid(column = 4,row=0)
          ttk.Button(algorithmFrame, text="Check!", command=lambda: self.check()).grid(column = 4,row=1)

     def setNum(self, num:int) -> None:
          self.board.num = num
          if num == -1:
               self.selectedNumDisplay.set(f"Selected: Delete")
          else:
               self.selectedNumDisplay.set(f"Selected: {num}")
     def setAlgo(self, algo:int) -> None:
          self.algorithm = algo
     def solve(self) -> None:
          match self.algorithm:
               case 0:
                    return self.board.naive()
               case 1:
                    pass
               case 2:
                    pass
               case 3:
                    pass
     def check(self) -> None:
          success = self.board.check()
          win = Toplevel(self.root)
          win.title("Result")
          win.geometry("100x30")
          win.resizable(FALSE,FALSE)
          frame = ttk.Frame(win,padding="2 2 2 2")
          frame.grid(column=0,row=0)
          statusText = " check!"
          if success:
               statusText = "Passed" + statusText
          else:
               statusText = "Failed" + statusText
          ttk.Label(frame,text=statusText).grid(column=0,row=0)
     
     #TODO:
     #pressing number button sets a variable in window to the num
     # add copy paste ability from some format of numbers
     # could seperate out all the sudoku related functions into a seperate file and class, 
     # pass it in a 2d array reresentation of board, then worry about changing cells, avoids bloating board class