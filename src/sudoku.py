import math
from src.cell import Cell

class Sudoku():
     def __init__(self,cells:list[list[Cell]]):
          self.cells = cells

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
     def naive(self) -> None:
          changed = True
          while not self.check() and changed:
               #blocks any numbers that have been placed
               blockChanged = self.blockAll()
               singleChanged = self.nakedSingle()
               hiddenChanged = self.hiddenSingle()
               # if any of the strategies have done anything this iteration, we're not stuck
               changed =  blockChanged or singleChanged or hiddenChanged
          return self.cells
     def nakedSingle(self) -> bool:
          """Iterates over every cell, if they only have one possible value, sets the cell to that and draws the num"""
          changed = False
          for i in range(0,9):
               for j in range(0,9):
                    c = self.cells[i][j]
                    if not -1 in c.possible and len(c.possible) == 1:
                         c.setNum(c.possible[0])
                         changed = True
          return changed
     def hiddenSingle(self) -> bool:
          """Iterates over every row, column and box, if there is only one cell that has a possiblity for a given number (even if that cell has other possiblities), set it to that"""
          #TODO:
          #either find a way to stop the same cell being accessed after it has been assigned, or split row/col/box to run in series not parallel
          changed = True
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
                              rowPossible[k].append(j)
                         if k in col[j].possible:
                              colPossible[k].append(j)
                         if k in box[j].possible:
                              boxPossible[k].append(j)
               #print(f"i: {i} rowPossible: {rowPossible}, colPossible: {colPossible}, boxPossible: {boxPossible}")
               #if there is only one possiblity for a given number in the row/col/box, find the cell that has that possibility and set it to the number
               for l in range(1,10):
                    if len(rowPossible[l]) == 1:
                         row[rowPossible[l][0]].setNum(l)
                         print(f"row #{i+1}, col#{rowPossible[l][0]+1} set to: {l}")
                         changed = True
                    if len(colPossible[l]) == 1:
                         col[colPossible[l][0]].setNum(l)
                         print(f"col#{i+1}, row #{colPossible[l][0]+1} set to: {l}")
                         changed = True
                    if len(boxPossible[l]) == 1:
                         box[boxPossible[l][0]].setNum(l)
                         print(f"item#{boxPossible[l][0]+1}, in box{i+1} set to: {l}")
                         changed = True
          return changed
     def nakedPairs(self) -> bool:
          """Iterates over every box, if there is a pair of cells in a row/col that have only the same two possiblities, remove possiblities of them from the box and row/col respectively"""
          stuck = True
          for i in range(0,9):
               box = self.getBox(i)
               #abandon all hope ye who enter here
               row1Pairs,row1Indices,row2Pairs,row2Indices,row3Pairs,row3Indices,col1Pairs,col1Indices,col2Pairs,col2Indices,col3Pairs,col3Indices = [],[],[],[],[],[],[],[],[],[],[],[]
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
               if len(row1Pairs) == 2 and row1Pairs[0] == row1Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0],boxPos[1]+row1Indices[0],row1Pairs[0], col=False)
                    self.blockMultiple(boxPos[0],boxPos[1]+row1Indices[1],row1Pairs[0], col=False)
                    stuck = False
               if len(row2Pairs) == 2 and row2Pairs[0] == row2Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+1,boxPos[1]+row2Indices[0],row2Pairs[0], col=False)
                    self.blockMultiple(boxPos[0]+1,boxPos[1]+row2Indices[1],row2Pairs[0], col=False)
                    stuck = False
               if len(row3Pairs) == 2 and row3Pairs[0] == row3Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+2,boxPos[1]+row3Indices[0],row3Pairs[0], col=False)
                    self.blockMultiple(boxPos[0]+2,boxPos[1]+row3Indices[1],row3Pairs[0], col=False)
                    stuck = False
               if len(col1Pairs) == 2 and col1Pairs[0] == col1Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+col1Indices[0],boxPos[1],col1Pairs[0], row=False)
                    self.blockMultiple(boxPos[0]+col1Indices[1],boxPos[1],col1Pairs[0], row=False)
                    stuck = False
               if len(col2Pairs) == 2 and col2Pairs[0] == row2Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+col2Indices[0],boxPos[1]+1,col2Pairs[0], row=False)
                    self.blockMultiple(boxPos[0]+col2Indices[1],boxPos[1]+1,col2Pairs[0], row=False)
                    stuck = False
               if len(col3Pairs) == 2 and col3Pairs[0] == col3Pairs[1]:
                    boxPos = self.getBoxPos(i)
                    self.blockMultiple(boxPos[0]+col3Indices[0],boxPos[1]+1,col3Pairs[0], row=False)
                    self.blockMultiple(boxPos[0]+col3Indices[1],boxPos[1]+1,col3Pairs[0], row=False)
                    stuck = False
          return stuck
     def hiddenPairs(self) -> bool:
               changed = False
               

               return changed
     def virtualPairs(self) -> bool:
          changed = False
          

          return changed
     def blockAll(self) -> bool:
          """Iterates over board, calling self.block() on any cells that haven't blocked yet and have a value"""
          c = False
          for i in range(0,9):
               for j in range(0,9):
                    c = self.cells[i][j]
                    if c.num > 0 and not c.hasBlocked:
                         changed = self.block(i,j,c.num)
                         c.hasBlocked = True
                         if changed:
                              c = True
          return c         
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
               if row and num in r[k].possible:
                    r[k].possible.remove(num)
                    changed = True
               if col and num in c[k].possible:
                    c[k].possible.remove(num)
                    changed = True
               if box and num in b[k].possible:
                    b[k].possible.remove(num)
                    changed = True
          return changed
     def blockMultiple(self, i, j, nums:list[int], row = True, col = True, box = True) -> bool:
          """Removes the input nums from the list of possible numbers in the column, row, and box of the input coordinate"""
          ret = []
          for n in nums:
               ret.append(self.block(i,j,n,row,col,box))
          return True in ret
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
     def updateSudoku(self, cells:list[list[Cell]]) -> None:
          self.cells = cells
     def getAllPossibles(self) -> list[list[list[int]]]:
          ret = []
          for i in range(0,9):
               ret.append([])
               for j in range(0,9):
                    ret[i].append(self.cells[i][j].possible)
          return ret
     
     #TODO: 
     #solving functions should return a list of moves made, for displaying to user