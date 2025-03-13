from cell import Cell, LineType
from tkinter import *
from tkinter import ttk
from sudoku import Sudoku
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
          self.setupSudoku()
          self.actions = []           
     def addNum(self, event) -> None:
          """Handles a click event on the canvas, and renders a number in the center of the cell that was clicked. If the number is -1, deletes the number in the cell."""
          x,y = event.x, event.y
          if x > self.xOffset and x < self.xOffset + (self.cellSizeX * 9) and y > self.yOffset and y < self.yOffset + (self.cellSizeY * 9):
               xindex = math.floor((x-self.xOffset)/self.cellSizeX)
               yindex = math.floor((y-self.yOffset)/self.cellSizeY)
               try:
                    self.cells[yindex][xindex].setNum(self.num)
                    if self.num == -1:
                         self.cells[yindex][xindex].delNum()
                         self.cells[yindex][xindex].eraseNum(self)
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
                    cell = Cell(i,j,(x1,y1),(x2,y2))
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
          self.actions = self.sudoku.naive()
          self.updateNums()
     def advanced(self) -> None:
          self.actions = self.sudoku.advanced()
          self.updateNums()
     def setupSudoku(self) -> None:
          self.sudoku = Sudoku(self.cells)

     def generatePossible(self):
          self.sudoku.blockAll()
          for i in range(0,9):
               for j in range(0,9):
                    self.sudoku.cells[i][j].drawPossible(self)
     def updateNums(self) -> None:
          """Draws the number for each cell in the board object"""
          for i in range(0,9):
               for j in range(0,9):
                    self.cells[i][j].drawNum(self)
     def clear(self) -> None:
          for i in range(0,9):
               for j in range(0,9):
                    self.cells[i][j].delNum()
                    self.cells[i][j].erasePossible(self)
                    self.cells[i][j].eraseNum(self)
          self.sudoku.updateSudoku(self.cells)
     def test(self):
          nums = [
               [1,-1, -1,   6,7,-1,   -1,-1, 2],
               [5, 7, 3,    1, 9, 2,  -1, 6,-1],
               [-1,-1,-1,  -1, 4,-1,  -1,-1, 7],

               [ -1,8, -1,  9,-1,-1,  3,-1,-1],
               [ -1,-1,-1, -1,-1,-1,  -1,-1,-1],
               [ 4,-1, -1, -1, 3,-1,  7,8, -1],

               [-1,-1,-1,  -1,5 ,-1,   6,-1, 3],
               [-1,-1, 5,  -1,-1,-1,  -1,-1,-1],
               [-1, 2, 9,  -1,8 ,-1,  -1, 4,-1],
          ]
          for i in range(0,9):
               for j in range(0,9):
                    self.cells[i][j].setNum(nums[i][j])
                    self.cells[i][j].drawNum(self)
          