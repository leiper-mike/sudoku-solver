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


     def setupAndDrawCells(self) -> None:
          """Creates a 2d array of cell objects, determines whether to bold a line edge of the cell depending on if it is on the edge of a box, and draws the cell on the canvas"""
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
     def check(self) -> bool:
          """Checks that the board meets the requirements of a completed sudoku puzzle: 1-9 only occur once in each column, row, and box"""
          for i in range(0,9):
               colNums = list(sorted(map(lambda c: c.num,self.getCol(i))))
               rowNums = list(sorted(map(lambda c: c.num,self.getRow(i))))
               boxNums = list(sorted(map(lambda c: c.num,self.getBox(i))))
               oneNine = list(range(1,10))
               # check that each row and col contain 1-9
               if colNums != oneNine or rowNums != oneNine or boxNums != oneNine:
                    return False
          return True
     def getCol(self, index:int) -> list[Cell]:
          """Returns a list of cells at the given column index"""              
          ret = []
          for i in range(0,9):
              ret.append(self.cells[i][index])
          return ret           
     def getRow(self,index:int) -> list[Cell]:
          """Returns a list of cells at the given row index"""   
          ret = []
          for i in range(0,9):
              ret.append(self.cells[index][i])
          return ret
     def getBox(self,index:int) -> list[Cell]:
          """Returns a list of cells at the given box index, starting at 0 in the top left and incrementing by 1 going right, ending at 8 in the bottom right"""   
          i = (math.floor(index / 3)) * 3
          j = (index % 3) * 3
          ret = []
          for k in range(i,i+3):
               for l in range(j,j+3):
                    ret.append(self.cells[k][l])
          return ret
     def getBoxPos(self, index:int) -> tuple[int,int]:
          return ((math.floor(index / 3)) * 3, (index % 3) * 3)
     def getBoxFromPos(self, i, j) -> list[Cell]:
          """Returns a list of cells from the box that the given coordinate is in"""
          i = math.floor(i / 3) * 3
          j = math.floor(j / 3) * 3
          ret = []
          for k in range(i,i+3):
               for l in range(j,j+3):
                    ret.append(self.cells[k][l])
          return ret
     def naive(self) -> None:
          stuck = False
          while not self.check() and not stuck:
               #blocks any numbers that have been placed
               blockStuck = self.blockAll()
               singleStuck = self.nakedSingle()
               hiddenStuck = self.hiddenSingle()
               # if any of the strategies have done anything this iteration, we're not stuck
               stuck = blockStuck and singleStuck and hiddenStuck
     def blockAll(self) -> bool:
          """Iterates over board, calling self.block() on any cells that haven't blocked yet and have a value"""
          stuck = True
          for i in range(0,9):
               for j in range(0,9):
                    c = self.cells[i][j]
                    if c.num > 0 and not c.hasBlocked:
                         changed = self.block(i,j)
                         c.hasBlocked = True
                         if changed:
                              stuck = False
          return stuck
     def nakedSingle(self) -> bool:
          """Iterates over every cell, if they only have one possible value, sets the cell to that and draws the num"""
          stuck = True
          for i in range(0,9):
               for j in range(0,9):
                    c = self.cells[i][j]
                    if not -1 in c.possible and len(c.possible) == 1:
                         c.num = c.possible[0]
                         c.drawNum(self)
                         stuck = False
          return stuck
     def hiddenSingle(self) -> bool:
          """Iterates over every row, column and box, if there is only one cell that has a possiblity for a given number (even if that cell has other possiblities), set it to that"""
          stuck = True
          for i in range(0,9):
               row = self.getRow(i)
               col = self.getCol(i)
               box = self.getBox(i)
               #key: possibility of cell, value: cells that have that possiblity
               rowPossible = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
               colPossible = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
               boxPossible = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
               #gets the total possibilities of row,col,box
               for j in range(0,9):
                    for k in range(1,10):
                         if k in row[j].possible:
                              rowPossible[k] = j
                         if k in col[j].possible:
                              colPossible[k] = j
                         if k in box[j].possible:
                              boxPossible[k] = j
               #if there is only one possiblity for a given number in the row/col/box, find the cell that has that possibility and set it to the number
               for l in range(1,10):
                    if len(rowPossible[l]) == 1:
                         row[rowPossible[l][0]].num = l
                         row[rowPossible[l][0]].drawNum(self)
                         stuck = False
                    if len(colPossible[l]) == 1:
                         col[colPossible[l][0]].num = l
                         col[colPossible[l][0]].drawNum(self)
                         stuck = False
                    if len(boxPossible[l]) == 1:
                         box[boxPossible[l][0]].num = l
                         box[boxPossible[l][0]].drawNum(self)
                         stuck = False
          return stuck
     
     def nakedPairs(self) -> bool:
          """Iterates over every box, if there is a pair of cells in a row/col that have only the same two possiblities, remove possiblities of them from the box and row/col respectively"""
          stuck = True
          for i in range(0,9):
               box = self.getBox(i)
               #abandon all hope ye who enter here
               row1Pairs, row1Indices,row2Pairs,row2Indices,row3Pairs,row3Indices,col1Pairs,col1Indices,col2Pairs,col2Indices,col3Pairs,col3Indices = [],[],[],[],[],[],[],[],[],[],[],[]
               row1 = box[:3]
               row2 = box[3:6]
               row3 = box[6:9]
               col1 = box[:7:3]
               col2 = box[1:8:3]
               col3 = box[2:9:3]
               for j in range(0,3):
                    if len(row1[j].possible) == 2:
                         row1Pairs.append(row1[j].possible)
                         row1Indices.append(j)
                    if len(row2[j].possible) == 2:
                         row2Pairs.append(row2[j].possible)
                         row2Indices.append(j)
                    if len(row3[j].possible) == 2:
                         row3Pairs.append(row3[j].possible)
                         row3Indices.append(j)
                    if len(col1[j].possible) == 2:
                         col1Pairs.append(col1[j].possible)
                         col1Indices.append(j)
                    if len(col2[j].possible) == 2:
                         col2Pairs.append(col2[j].possible)
                         col2Indices.append(j)
                    if len(col3[j].possible) == 2:
                         col3Pairs.append(col3[j].possible)
                         col3Indices.append(j)
               #check that there are two pairs and they are the same pair, blocks row/column respectively and box
               if len(row1Pairs == 2) and row1Pairs[0] == row1Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0],boxPos[1]+row1Indices[0],row1Pairs[0], col=False)
                    self.blockMultiple(boxPos[0],boxPos[1]+row1Indices[1],row1Pairs[0], col=False)
                    stuck = False
               if len(row2Pairs == 2) and row2Pairs[0] == row2Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+1,boxPos[1]+row2Indices[0],row2Pairs[0], col=False)
                    self.blockMultiple(boxPos[0]+1,boxPos[1]+row2Indices[1],row2Pairs[0], col=False)
                    stuck = False
               if len(row3Pairs == 2) and row3Pairs[0] == row3Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+2,boxPos[1]+row3Indices[0],row3Pairs[0], col=False)
                    self.blockMultiple(boxPos[0]+2,boxPos[1]+row3Indices[1],row3Pairs[0], col=False)
                    stuck = False
               if len(col1Pairs == 2) and col1Pairs[0] == col1Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+col1Indices[0],boxPos[1],col1Pairs[0], row=False)
                    self.blockMultiple(boxPos[0]+col1Indices[1],boxPos[1],col1Pairs[0], row=False)
                    stuck = False
               if len(col2Pairs == 2) and col2Pairs[0] == row2Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+col2Indices[0],boxPos[1]+1,col2Pairs[0], row=False)
                    self.blockMultiple(boxPos[0]+col2Indices[1],boxPos[1]+1,col2Pairs[0], row=False)
                    stuck = False
               if len(col3Pairs == 2) and col3Pairs[0] == col3Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+col3Indices[0],boxPos[1]+1,col3Pairs[0], row=False)
                    self.blockMultiple(boxPos[0]+col3Indices[1],boxPos[1]+1,col3Pairs[0], row=False)
                    stuck = False
          return stuck
     def hiddenPairs(self) -> bool:
               stuck = True
               

               return stuck
     def virtualPairs(self) -> bool:
          stuck = True
          

          return stuck
               
     def block(self, i, j, num, row = True, col = True, box = True) -> bool:
          """Removes the input num from the list of possible numbers in the column, row, and box of the input coordinate"""
          r = None
          if row:
               r = self.getRow(i)
          c = None
          if col:
               c = self.getCol(j)
          b = None
          if box:
               b = self.getBoxFromPos(i,j)
          changed = False
          for k in range(0,9):
               if row and num in row[k].possible:
                    row[k].possible.remove(num)
                    changed = True
               if col and num in col[k].possible:
                    col[k].possible.remove(num)
                    changed = True
               if box and num in box[k].possible:
                    box[k].possible.remove(num)
                    changed = True
          return changed
     def blockMultiple(self, i, j, nums:list[int], row = True, col = True, box = True) -> bool:
          """Removes the input num from the list of possible numbers in the column, row, and box of the input coordinate"""
          r = None
          if row:
               r = self.getRow(i)
          c = None
          if col:
               c = self.getCol(j)
          b = None
          if box:
               b = self.getBoxFromPos(i,j)
          changed = False
          for k in range(0,9):
               for n in nums:
                    if row and n in row[k].possible:
                         row[k].possible.remove(n)
                         changed = True
                    if col and n in col[k].possible:
                         col[k].possible.remove(n)
                         changed = True
                    if box and n in box[k].possible:
                         box[k].possible.remove(n)
                         changed = True
          return changed