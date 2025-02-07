from cell import Cell, LineType
from tkinter import *
from tkinter import ttk
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


     def setupAndDrawCells(self) -> None:
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
                    cell.draw(self)
                    self.cells[i].append(cell)

                    
                    
                    
     