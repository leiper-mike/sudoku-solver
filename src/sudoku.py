import math
from cell import Cell

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
     def naive(self) -> list[str]:
          changed = True
          actions = []
          limit = 1
          while not self.check() and limit >= 0:
               size = len(actions)
               #blocks any numbers that have been placed
               actions.extend(self.blockAll())
               actions.extend(self.nakedSingle())
               actions.extend(self.hiddenSingle())

               actions.extend(self.nakedPairs())
               actions.extend(self.hiddenPairs())
               actions.extend(self.virtualSingle())
               # if none of the strategies have taken an action in the last two iterations, we're stuck, exit
               changed = size != len(actions)
               if not changed:
                    limit-=1
               else:
                    limit = 1
          return actions
     def nakedSingle(self) -> list[str]:
          """Iterates over every cell, if they only have one possible value, sets the cell to that and draws the num"""
          actions = []
          for i in range(0,9):
               for j in range(0,9):
                    c = self.cells[i][j]
                    if not -1 in c.possible and len(c.possible) == 1:
                         num = c.possible[0]
                         c.setNum(num)
                         self.block(i,j,num)
                         actions.append(f"Naked Single: Cell at Row: {i+1}, Column: {j+1} set to {num}")
          return actions
     def hiddenSingle(self) -> list[str]:
          """Iterates over every row, column and box, if there is only one cell that has a possiblity for a given number (even if that cell has other possiblities), set it to that"""
          actions = []
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
               #if there is only one possiblity for a given number in the row/col/box, find the cell that has that possibility and set it to the number
               for l in range(1,10):
                    if len(rowPossible[l]) == 1:
                         row[rowPossible[l][0]].setNum(l)
                         self.block(i, rowPossible[l][0],l)
                         actions.append(f"Hidden Single: row #{i+1}, col#{rowPossible[l][0]+1} set to: {l}")
               #col
               for j in range(0,9):
                    for k in range(1,10):
                         if k in col[j].possible:
                              colPossible[k].append(j)
               for l in range(1,10):
                    if len(colPossible[l]) == 1:
                         col[colPossible[l][0]].setNum(l)
                         self.block(colPossible[l][0],i,l)
                         actions.append(f"Hidden Single: col#{i+1}, row #{colPossible[l][0]+1} set to: {l}")
               #box
               for j in range(0,9):
                    for k in range(1,10):
                         if k in box[j].possible:
                              boxPossible[k].append(j)
               for l in range(1,10):
                    if len(boxPossible[l]) == 1:
                         box[boxPossible[l][0]].setNum(l)
                         i1, j1 = self.boxRelativeToAbsoluteCoords(i,boxPossible[l][0])
                         self.block(i1, j1, l) 
                         actions.append(f"Hidden Single: item#{boxPossible[l][0]+1}, in box{i+1} set to: {l}")
          return actions
     def nakedPairs(self) -> bool:
          """Iterates over every box, if there is a pair of cells in a row/col that have only the same two possiblities, remove possiblities of them from the box and row/col respectively"""
          actions = []
          for i in range(0,9):
               box = self.getBox(i)
               #abandon all hope ye who enter here
               r1P,r1I,r2P,r2I,r3P,r3I,c1P,c1I,c2P,c2I,c3P,c3I = [],[],[],[],[],[],[],[],[],[],[],[]
               row1 = box[:3]
               row2 = box[3:6]
               row3 = box[6:9]
               col1 = box[:7:3]
               col2 = box[1:8:3]
               col3 = box[2:9:3]
               for j in range(0,3):
                    #if there are only 2 possiblities in a cell
                    if len(row1[j].possible) == 2:
                         #add the possibilites to an array, save the index
                         r1P.append(row1[j].possible)
                         r1I.append(j)
                    if len(row2[j].possible) == 2:
                         r2P.append(row2[j].possible)
                         r2I.append(j)
                    if len(row3[j].possible) == 2:
                         r3P.append(row3[j].possible)
                         r3I.append(j)
                    if len(col1[j].possible) == 2:
                         c1P.append(col1[j].possible)
                         c1I.append(j)
                    if len(col2[j].possible) == 2:
                         c2P.append(col2[j].possible)
                         c2I.append(j)
                    if len(col3[j].possible) == 2:
                         c3P.append(col3[j].possible)
                         c3I.append(j)
               #check that there are two pairs and they are the same pair, blocks row/column respectively and box
               i1,j1 = self.getBoxPos(i)
               if len(r1P) == 2 and r1P[0] == r1P[1]:
                    self.cells[i1][j1+r1I[0]].hasBlocked = True
                    self.cells[i1][j1+r1I[1]].hasBlocked = True

                    stat1 = self.blockMultiple(i1,j1+r1I[0],r1P[0], col=False)
                    self.cells[i1][j1+r1I[1]].possible = r1P[0]
                    stat2 = self.blockMultiple(i1,j1+r1I[1],r1P[0], col=False)
                    #allow them to be blocked again
                    self.cells[i1][j1+r1I[0]].hasBlocked = False
                    self.cells[i1][j1+r1I[1]].hasBlocked = False
                    if stat1 or stat2:
                         actions.append(f"Naked Pair: Cells {i1+1},{j1+r1I[0]+1} and {i1+1},{j1+r1I[1]+1}, eliminating {r1P[0]} in row {i1+1} and box #{i+1}")
               if len(r2P) == 2 and r2P[0] == r2P[1]:
                    self.cells[i1+1][j1+r2I[0]].hasBlocked = True
                    self.cells[i1+1][j1+r2I[1]].hasBlocked = True

                    stat1 = self.blockMultiple(i1+1,j1+r2I[0],r2P[0], col=False)
                    self.cells[i1+1][j1+r2I[1]].possible = r2P[0]
                    stat2 = self.blockMultiple(i1+1,j1+r2I[1],r2P[0], col=False)

                    self.cells[i1+1][j1+r2I[0]].hasBlocked = False
                    self.cells[i1+1][j1+r2I[1]].hasBlocked = False
                    if stat1 or stat2:
                         actions.append(f"Naked Pair: Cells {i1+2},{j1+r2I[0]+1} and {i1+2},{j1+r2I[1]+1}, eliminating {r2P[0]} in row {i1+2} and box #{i+1}")
               if len(r3P) == 2 and r3P[0] == r3P[1]:
                    self.cells[i1+2][j1+r3I[0]].hasBlocked = True
                    self.cells[i1+2][j1+r3I[1]].hasBlocked = True

                    stat1 = self.blockMultiple(i1+2,j1+r3I[0],r3P[0], col=False)
                    self.cells[i1+2][j1+r3I[1]].possible = r3P[0]
                    stat2 = self.blockMultiple(i1+2,j1+r3I[1],r3P[0], col=False)

                    self.cells[i1+2][j1+r3I[0]].hasBlocked = False
                    self.cells[i1+2][j1+r3I[1]].hasBlocked = False
                    if stat1 or stat2:
                         actions.append(f"Naked Pair: Cells {i1+3},{j1+r3I[0]+1} and {i1+3},{j1+r3I[1]+1}, eliminating {r3P[0]} in row {i1+3} and box #{i+1}")
               if len(c1P) == 2 and c1P[0] == c1P[1]:
                    self.cells[i1+c1I[0]][j1].hasBlocked = True
                    self.cells[i1+c1I[1]][j1].hasBlocked = True

                    stat1 = self.blockMultiple(i1+c1I[0],j1,c1P[0], row=False)
                    self.cells[i1+c1I[1]][j1].possible = c1P[0]
                    stat2 = self.blockMultiple(i1+c1I[1],j1,c1P[0], row=False)

                    self.cells[i1+c1I[0]][j1].hasBlocked = False
                    self.cells[i1+c1I[1]][j1].hasBlocked = False
                    if stat1 or stat2:
                         actions.append(f"Naked Pair: Cells {i1+c1I[0]+1},{j1+1} and {i1+c1I[1]+1},{j1+1}, eliminating {c1P[0]} in col {j1+1} and box #{i+1}")
               if len(c2P) == 2 and c2P[0] == c2P[1]:
                    self.cells[i1+c2I[0]][j1+1].hasBlocked = True
                    self.cells[i1+c2I[1]][j1+1].hasBlocked = True

                    stat1 = self.blockMultiple(i1+c2I[0],j1+1,c2P[0], row=False)
                    self.cells[i1+c2I[1]][j1+1].possible = c2P[0]
                    stat2 = self.blockMultiple(i1+c2I[1],j1+1,c2P[0], row=False)

                    self.cells[i1+c2I[0]][j1+1].hasBlocked = False
                    self.cells[i1+c2I[1]][j1+1].hasBlocked = False
                    if stat1 or stat2:
                         actions.append(f"Naked Pair: Cells {i1+c2I[0]+1},{j1+2} and {i1+c2I[1]+1},{j1+2}, eliminating {c2P[0]} in col {j1+2} and box #{i+1}")
               if len(c3P) == 2 and c3P[0] == c3P[1]:
                    self.cells[i1+c3I[0]][j1+2].hasBlocked = True
                    self.cells[i1+c3I[1]][j1+2].hasBlocked = True
               
                    stat1 = self.blockMultiple(i1+c3I[0],j1+2,c3P[0], row=False)
                    self.cells[i1+c3I[1]][j1+2].possible = c3P[0]
                    stat2 = self.blockMultiple(i1+c3I[1],j1+2,c3P[0], row=False)

                    self.cells[i1+c3I[0]][j1+2].hasBlocked = False
                    self.cells[i1+c3I[1]][j1+2].hasBlocked = False
                    if stat1 or stat2:
                         actions.append(f"Naked Pair: Cells {i1+c3I[0]+1},{j1+3} and {i1+c3I[1]+1},{j1+3}, eliminating {c3P[0]} in col {j1+3} and box #{i+1}")
          return actions
     def hiddenPairs(self) -> bool:
          """Iterates over every box, and finds pairs of possible numbers, eliminating other possibilities on those cells"""
          actions = []
          for i in range(0,9):
               box = self.getBox(i)
               possibles = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
               for j in range(0,9):
                    for k in range(1,10):
                         if k in box[j].possible and possibles[k] != [-1]:
                              # if there were going to be more than 3 cells with the value, don't care about that value
                              if len(possibles[k]) == 2:
                                   possibles[k] = [-1]
                              else:
                                   possibles[k].append(j)
               
               for key, value in possibles.items():
                    #exclude singles
                    if len(value) == 2:
                         #search rest of possibilities
                         for l in range(key+1,10):
                              # if a pair is found
                              if value == possibles[l]:
                                   #set their possible values to only their shared values (the hidden pair)
                                   size1 = len(box[value[0]].possible)
                                   size2 = len(box[value[1]].possible)
                                   box[value[0]].possible = [key,l]
                                   box[value[1]].possible = [key,l]
                                   if len(box[value[0]].possible) != size1 or len(box[value[0]].possible) != size2:
                                        actions.append(f"Hidden pair: Cells #{value[0]+1},{value[1]+1} in box #{i+1} are the only cells to contain both {key} and {l}, therefore they must be one of the two")
          return actions
     def virtualSingle(self) -> bool:
          actions = []
          for i in range(0,9):
               box = self.getBox(i)
               possibles = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
               for j in range(0,9):
                    for k in range(1,10):
                         if k in box[j].possible and possibles[k] != [-1]:
                              # if there were going to be more than 3 cells with the value, don't care about that value
                              if len(possibles[k]) == 2:
                                   possibles[k] = [-1]
                              else:
                                   possibles[k].append(j)
               # if a pair is in a row or col, block row/col with num
               for key, value in possibles.items():
                    #exclude singles
                    if len(value) == 2:
                         # same col
                         if value[0] % 3 == value[1] % 3:
                              bp = self.getBoxPos(i)
                              i1 = bp[0] + math.floor(value[0]/3)
                              j1 = bp[1] + value[0] % 3
                              i2 = bp[0] + math.floor(value[1]/3)
                              j2 = bp[1] + value[1] % 3
                              #prevent removing the pair
                              self.cells[i1][j1].hasBlocked = True
                              self.cells[i2][j2].hasBlocked = True
                              #block pair from col
                              status = self.block(i1,j1,key,row=False,box=False)
                              self.cells[i1][j1].hasBlocked = False
                              self.cells[i2][j2].hasBlocked = False
                              if status:
                                   actions.append(f"Virtual Single: Cells {i1+1},{j1+1} and {i2+1},{j2+1} are the only cells that contain {key}, and are in a column in box #{i+1}, removing possibilities of {key} in column {j1+1}")

                         elif math.floor(value[0]/3) == math.floor(value[1]/3):
                              bp = self.getBoxPos(i)
                              i1 = bp[0] + math.floor(value[0]/3)
                              j1 = bp[1] + value[0] % 3
                              i2 = bp[0] + math.floor(value[1]/3)
                              j2 = bp[1] + value[1] % 3
                              #prevent removing the pair
                              self.cells[i1][j1].hasBlocked = True
                              self.cells[i2][j2].hasBlocked = True
                              #block pair from row
                              status = self.block(i1,j1,key,col=False,box=False)
                              self.cells[i1][j1].hasBlocked = False
                              self.cells[i2][j2].hasBlocked = False
                              if status:
                                   actions.append(f"Virtual Single: Cells {i1+1},{j1+1} and {i2+1},{j2+1} are the only cells that contain {key}, and are in a row in box #{i+1}, removing possibilities of {key} in row {i1+1}")


          return actions
     def blockAll(self) -> bool:
          """Iterates over board, calling self.block() on any cells that haven't blocked yet and have a value"""
          actions = []
          for i in range(0,9):
               for j in range(0,9):
                    cell = self.cells[i][j]
                    if cell.num > 0 and not cell.hasBlocked:
                         changed = self.block(i,j,cell.num)
                         cell.hasBlocked = True
                         if changed:
                              actions.append(f"Blocking: cell at {i+1},{j+1} blocked {cell.num}")
          return actions         
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
               #check row is enabled, that the current cell hasn't blocked, that the current cell has the num being blocked as a possibility, and that the cell isn't the one we're blocking from
               if row and not r[k].hasBlocked and num in r[k].possible and self.cells[i][j] != r[k]:
                    r[k].possible.remove(num)
                    changed = True
               if col and not c[k].hasBlocked and num in c[k].possible and self.cells[i][j] != c[k]:
                    c[k].possible.remove(num)
                    changed = True
               if box and not b[k].hasBlocked and num in b[k].possible and self.cells[i][j] != b[k]:
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
     def getPossibles(self, index=-1, row=False, col=False, box=False) -> list[list[list[int]]]:
          ret = []
          if row:
               for i in range(0,9):
                    ret[0].append(self.cells[index][i].possible)
          elif col:
               for i in range(0,9):
                    ret[0].append(self.cells[i][index].possible)
          elif box:
               box = self.getBox(index)
               for c in box:
                    ret[0].append(c.possible)
          else:
               for i in range(0,9):
                    ret.append([])
                    for j in range(0,9):
                         ret[i].append(self.cells[i][j].possible)
          return ret
     def boxRelativeToAbsoluteCoords(self, boxIndex:int, cellIndex:int) -> tuple[int,int]:
          return (math.floor(boxIndex / 3) * 3 + (math.floor(cellIndex/3)),(boxIndex % 3) * 3 + (cellIndex % 3))

     #TODO:
     # add a setnum func to sudoku, blocks num after assigning
     # hidden single set col 2 row 8 to 3



