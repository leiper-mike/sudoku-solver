from src.cell import Cell, LineType
from tkinter import *
from tkinter import ttk
from src.sudoku import Sudoku
import math
class Board(Canvas):
     def __init__(self, parent, lineColor:str = "black", **kwargs)-> None:
          super().__init__(parent,**kwargs)
          self.bind("<Button-1>", self.addNum)
          self.xOffset = 5
          self.yOffset = 5
          self.cellSizeX = 30
          self.cellSizeY = 30
          self.lineColor = lineColor
          self.num = 1
          self.cells = []                        
                         
     def addNum(self, event) -> None:
          """Handles a click event on the canvas, and renders a number in the center of the cell that was clicked. If the number is -1, deletes the number in the cell."""
          x,y = event.x, event.y
          if x > self.xOffset and x < self.xOffset + (self.cellSizeX * 9) and y > self.yOffset and y < self.yOffset + (self.cellSizeY * 9):
               xindex = math.floor((x-self.xOffset)/self.cellSizeX)
               yindex = math.floor((y-self.yOffset)/self.cellSizeY)
               try:
                    self.cells[yindex][xindex].num = self.num
                    if self.num == -1:
                         self.cells[yindex][xindex].delNum(self)
                    else:
                         self.cells[yindex][xindex].drawNum(self)
               except IndexError:
                    return


     def setupCells(self) -> None:
          """Creates a 2d array of cell objects, determines whether to bold a line edge of the cell depending on if it is on the edge of a box"""
          for i in range(0,9):
               y1 = self.yOffset + (self.cellSizeY * i)
               self.cells.append([])
               for j in range(0,9):
                    x1 = self.xOffset + (self.cellSizeX * j)
                    x2 = x1+self.cellSizeX
                    y2 = y1+self.cellSizeY
                    cell = Cell((x1,y1),(x2,y2))
                    lineTypes = []
                    #makes lines thicker to delineate boxes and edge of board
                    # top line
                    if i == 0 or i == 3 or i == 6:
                         lineTypes.append(LineType.TOP)
                    #bottom line
                    if i == 8:
                         lineTypes.append(LineType.BOTTOM)
                    #left line
                    if j == 0 or j == 3 or j == 6:
                         lineTypes.append(LineType.LEFT)
                    #right line
                    if j == 8:
                         lineTypes.append(LineType.RIGHT)
                    cell.lineTypes = lineTypes
                    self.cells[i].append(cell)
     def drawCells(self) -> None:
          """Draws all the cells in the board object"""
          for i in range(0,9):
               for j in range(0,9):
                    self.cells[i][j].draw(self)
     def check(self) -> bool:
          """Checks that the board meets the requirements of a completed sudoku puzzle: 1-9 only occur once in each column, row, and box"""
          self.sudoku.updateSudoku(self.cells)
          return self.sudoku.check()
     def naive(self) -> None:
          self.cells = self.sudoku.naive()
     def setupSudoku(self) -> None:
          self.sudoku = Sudoku(self.cells)
     