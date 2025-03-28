import math
from cell import Cell
from enum import Enum
class MODE(Enum):
     ROW = 0,
     COLUMN = 1,
     BOX = 2,
     ALL = 3

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
               actions.extend(self.virtualSingle())
               actions.extend(self.virtualSingleBox())

               actions.extend(self.nakedPairs())
               actions.extend(self.hiddenPairs())
               # if none of the strategies have taken an action in the last two iterations, we're stuck, exit
               changed = size != len(actions)
               if not changed:
                    limit-=1
               else:
                    limit = 1
          return actions
     def advanced(self) -> list[str]:
          changed = True
          actions = []
          limit = 1
          while not self.check() and limit >= 0:
               size = len(actions)
               actions.extend(self.naive())
               actions.extend(self.nakedTriples())
               actions.extend(self.hiddenTriples())
               actions.extend(self.xWing())
               actions.extend(self.chuteRemotePairs())
               actions.extend(self.yWing())
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
                         self.block(i,j,num, MODE.ROW)
                         self.block(i,j,num, MODE.COLUMN)
                         self.block(i,j,num, MODE.BOX)
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
                         self.block(i, rowPossible[l][0],l, MODE.ROW)
                         self.block(i, rowPossible[l][0],l, MODE.COLUMN)
                         self.block(i, rowPossible[l][0],l, MODE.BOX)
                         actions.append(f"Hidden Single: row #{i+1}, col#{rowPossible[l][0]+1} set to: {l}")
               #col
               for j in range(0,9):
                    for k in range(1,10):
                         if k in col[j].possible:
                              colPossible[k].append(j)
               for l in range(1,10):
                    if len(colPossible[l]) == 1:
                         col[colPossible[l][0]].setNum(l)
                         self.block(colPossible[l][0],i,l, MODE.ROW)
                         self.block(colPossible[l][0],i,l, MODE.COLUMN)
                         self.block(colPossible[l][0],i,l, MODE.BOX)
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
                         self.block(i1, j1, l, MODE.ROW) 
                         self.block(i1, j1, l, MODE.COLUMN) 
                         self.block(i1, j1, l, MODE.BOX) 
                         actions.append(f"Hidden Single: item#{boxPossible[l][0]+1}, in box{i+1} set to: {l}")
          return actions
     def nakedPairs(self) -> list[str]:
          """Iterates over every box, if there is a pair of cells in a row/col/box that have only the same two possiblities, remove possiblities of them from the row/col/box"""
          actions = []
          for i in range(0,9):
               row = self.getRow(i)

               for j in range(0,8):
                    if not -1 in row[j].possible and len(row[j].possible) == 2:
                         for k in range(j+1,9):
                              if len(row[k].possible) == 2 and row[j].possible == row[k].possible:
                                   row[k].hasBlocked = True
                                   row[j].hasBlocked = True
                                   status = self.blockMultiple(i,0,row[j].possible,MODE.ROW)
                                   row[k].hasBlocked = False
                                   row[j].hasBlocked = False
                                   if status: 
                                        actions.append(f"Naked Pair: Cells {j+1},{k+1} in row {i+1} can only be {row[j].possible}, removing those candidates from the row")


               
          for i in range(0,9):
               col = self.getCol(i)

               for j in range(0,8):
                    if not -1 in col[j].possible and len(col[j].possible) == 2:
                         for k in range(j+1,9):
                              if len(col[k].possible) == 2 and col[j].possible == col[k].possible:
                                   col[k].hasBlocked = True
                                   col[j].hasBlocked = True
                                   status = self.blockMultiple(0,i,col[j].possible,MODE.COLUMN)
                                   col[k].hasBlocked = False
                                   col[j].hasBlocked = False
                                   if status: 
                                        actions.append(f"Naked Pair: Cells {j+1},{k+1} in col {i+1} can only be {col[j].possible}, removing those candidates from the column")
               

          for i in range(0,9):
               box = self.getBox(i)

               for j in range(0,8):
                    if not -1 in box[j].possible and len(box[j].possible) == 2:
                         for k in range(j+1,9):
                              if len(box[k].possible) == 2 and box[j].possible == box[k].possible:
                                   box[k].hasBlocked = True
                                   box[j].hasBlocked = True
                                   i1,j1 = self.boxRelativeToAbsoluteCoords(i,j)
                                   status = self.blockMultiple(i1,j1,box[j].possible,MODE.BOX)
                                   box[k].hasBlocked = False
                                   box[j].hasBlocked = False
                                   if status: 
                                        actions.append(f"Naked Pair: Cells {j+1},{k+1} in box {i+1} can only be {box[j].possible}, removing those candidates from the box")
              

          return actions
     def hiddenPairs(self) -> list[str]:
          """Iterates over every box, and finds pairs of possible numbers, eliminating other possibilities on those cells"""
          actions = []
          for i in range(0,9):
               row = self.getRow(i)

               rowPossible = self.getPossiblesDict(i,MODE.ROW,2,2)
               rowPairs = self.getNGroup(rowPossible,2,2)

               
               for rowPair in rowPairs:
                    diff = False
                    for index in rowPair[1]:
                         diff = diff or row[index].possible != rowPair[0]
                         row[index].possible = rowPair[0].copy()
                    if diff:
                         actions.append(f"Hidden pair: Cells {rowPair[1][0]+1},{rowPair[1][1]+1} in row {i+1} are the only cells in the row that contain: {rowPair[0]}, removing other candidates fromm those cells.")

          for i in range(0,9):
               col = self.getCol(i)

               colPossible = self.getPossiblesDict(i,MODE.COLUMN,2,2)
               colPairs = self.getNGroup(colPossible,2,2)

               for colPair in colPairs:
                    diff = False
                    for index in colPair[1]:
                         diff = diff or col[index].possible != colPair[0]
                         col[index].possible = colPair[0].copy()
                    if diff:
                         actions.append(f"Hidden pair: Cells {colPair[1][0]+1},{colPair[1][1]+1} in column {i+1} are the only cells in the column that contain: {colPair[0]}, removing other candidates fromm those cells.")

          for i in range(0,9):
               box = self.getBox(i)

               boxPossible = self.getPossiblesDict(i,MODE.BOX,2,2)
               boxPairs = self.getNGroup(boxPossible,2,2)

               for boxPair in boxPairs:
                    diff = False
                    for index in boxPair[1]:
                         diff = diff or box[index].possible != boxPair[0]
                         box[index].possible = boxPair[0].copy()
                    if diff:
                         actions.append(f"Hidden pair: Cells {boxPair[1][0]+1},{boxPair[1][1]+1} in box {i+1} are the only cells in the box that contain: {boxPair[0]}, removing other candidates fromm those cells.")
                         
          return actions
     def virtualSingle(self) -> list[str]:
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
                         elif -1 in box[j].possible:
                              break
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
                              status = self.block(i1,j1,key,MODE.COLUMN)
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
                              status = self.block(i1,j1,key,MODE.ROW)
                              self.cells[i1][j1].hasBlocked = False
                              self.cells[i2][j2].hasBlocked = False
                              if status:
                                   actions.append(f"Virtual Single: Cells {i1+1},{j1+1} and {i2+1},{j2+1} are the only cells that contain {key}, and are in a row in box #{i+1}, removing possibilities of {key} in row {i1+1}")
          return actions
     def virtualSingleBox(self) -> list[str]:
          actions = []
          #loop throw col/rows, get possible dict, if any with 2, check if in same box, block box 
          for i in range(0,9):
               rowP = self.getPossiblesDict(i,MODE.ROW,2,2)
               row = self.getRow(i)
               for j in range(1,10):
                    if not -1 in rowP[j]:
                         ind1, ind2 = self.getBoxIndexFromPos(i, rowP[j][0]), self.getBoxIndexFromPos(i, rowP[j][1])
                         if ind1 == ind2:
                              row[rowP[j][0]].hasBlocked = True
                              row[rowP[j][1]].hasBlocked = True
                              status = self.block(i,rowP[j][0],j,MODE.BOX)
                              row[rowP[j][0]].hasBlocked = False
                              row[rowP[j][1]].hasBlocked = False
                              if status:
                                   actions.append(f"Virtual pair: Cells {rowP[j][0]+1},{rowP[j][1] +1} in row {i+1} are the only cells that contain {j} in that row, and they are in the same box, no other cell in that box can be {j}")
          for i in range(0,9):
               colP = self.getPossiblesDict(i,MODE.COLUMN,2,2)
               col = self.getCol(i)
               for j in range(1,10):
                    if not -1 in colP[j]:
                         ind1, ind2 = self.getBoxIndexFromPos(i, colP[j][0]), self.getBoxIndexFromPos(i, colP[j][1])
                         if ind1 == ind2:
                              col[colP[j][0]].hasBlocked = True
                              col[colP[j][1]].hasBlocked = True
                              status = self.block(colP[j][0],i,j,MODE.BOX)
                              col[colP[j][0]].hasBlocked = False
                              col[colP[j][1]].hasBlocked = False
                              if status:
                                   actions.append(f"Virtual pair: Cells {colP[j][0]+1},{colP[j][1] +1} in column {i+1} are the only cells that contain {j} in that column, and they are in the same box, no other cell in that box can be {j}")
          return actions
     def nakedTriples(self) -> list[str]:
          """Iterates over every box, if there is a triplet of cells in a row/col/box that have only the same three possiblities, remove possiblities of them from the row/col/box"""
          actions = []
          for i in range(0,9):
               rowP = self.getPossibles(MODE.ROW,i)
               triplets = {}
               #get all naked triples
               for j in range(0,9):
                    if not -1 in rowP[j] and len(rowP[j]) == 3:
                         candidates = self.listToStr(rowP[j])
                         if not candidates in triplets:
                              triplets[candidates] = [j]
                         else:
                              triplets[candidates].append(j)
               #add any cells that are a subset of a naked triple, ex 1,5 and 5,9 are subsets of triple 1,5,9
               for k in range(0,9):
                    for key in triplets.keys():
                         if not -1 in rowP[k] and not k in triplets[key] and len(rowP[k]) == 2 and set(rowP[k]) <= set(self.strToIntList(key)):
                              triplets[key].append(k)
               #block
               row = self.getRow(i)
               for triplet, indices in triplets.items():
                         if len(indices) == 3:
                              indices = sorted(indices)
                              row = self.getRow(i)
                              for ind in indices:
                                   row[ind].hasBlocked = True
                              status = self.blockMultiple(i,0,self.strToIntList(triplet),MODE.ROW)
                              for ind in indices:
                                   row[ind].hasBlocked = False
                              if status: 
                                   actions.append(f"Naked Triple: Cells {indices[0]+1},{indices[1]+1},{indices[2]+1} in row {i+1} can only be {sorted(self.strToIntList(triplet))}, removing those candidates from the row")
          for i in range(0,9):
               colP = self.getPossibles(MODE.COLUMN,i)
               triplets = {}
               #get all naked triples
               for j in range(0,9):
                    if not -1 in colP[j] and len(colP[j]) == 3:
                         candidates = self.listToStr(colP[j])
                         if not candidates in triplets:
                              triplets[candidates] = [j]
                         else:
                              triplets[candidates].append(j)
               #add any cells that are a subset of a naked triple, ex 1,5 and 5,9 are subsets of triple 1,5,9
               for k in range(0,9):
                    for key in triplets.keys():
                         if not -1 in colP[k] and not k in triplets[key] and len(colP[k]) == 2 and set(colP[k]) <= set(self.strToIntList(key)):
                              triplets[key].append(k)
               #block
               col = self.getCol(i)
               for triplet, indices in triplets.items():
                         if len(indices) == 3:
                              indices = sorted(indices)
                              for ind in indices:
                                   col[ind].hasBlocked = True

                              status = self.blockMultiple(0,i,self.strToIntList(triplet),MODE.COLUMN)
                              for ind in indices:
                                   col[ind].hasBlocked = False
                              if status: 
                                   actions.append(f"Naked Triple: Cells {indices[0]+1},{indices[1]+1},{indices[2]+1} in column {i+1} can only be {self.strToIntList(triplet)}, removing those candidates from the column")
          for i in range(0,9):
               boxP = self.getPossibles(MODE.BOX,i)
               triplets = {}
               #get all naked triples
               for j in range(0,9):
                    if not -1 in boxP[j] and len(boxP[j]) == 3:
                         candidates = self.listToStr(boxP[j])
                         if not candidates in triplets:
                              triplets[candidates] = [j]
                         else:
                              triplets[candidates].append(j)
               #add any cells that are a subset of a naked triple, ex 1,5 and 5,9 are subsets of triple 1,5,9
               for k in range(0,9):
                    for key in triplets.keys():
                         if not -1 in boxP[k] and not k in triplets[key] and len(boxP[k]) == 2 and set(boxP[k]) <= set(self.strToIntList(key)):
                              triplets[key].append(k)
               #block
               box = self.getBox(i)
               for triplet, indices in triplets.items():
                         if len(indices) == 3:
                              indices = sorted(indices)
                              for ind in indices:
                                   box[ind].hasBlocked = True
                              i1,j1 = self.getBoxPos(i)
                              status = self.blockMultiple(i1,j1,self.strToIntList(triplet),MODE.BOX)
                              for ind in indices:
                                   box[ind].hasBlocked = False
                              if status: 
                                   actions.append(f"Naked Triple: Cells {indices[0]+1},{indices[1]+1},{indices[2]+1} in box {i+1} can only be {self.strToIntList(triplet)}, removing those candidates from the box")
          return actions
     def hiddenTriples(self) -> list[str]:
          actions = []
          for i in range(0,9):
               rowP = self.getPossiblesDict(i,MODE.ROW,2,3)
               #{"468":[1,5,7]}
               triples = {}
               for j in range(1,10):
                    if len(rowP[j]) == 3:
                         cells = self.listToStr(rowP[j])
                         triples[cells] = [j]
                         for k in range(1,10):
                              if  k != j and set(rowP[k]) <= set(self.strToIntList(cells)):
                                   triples[cells].append(k)

               for indices, triplet in triples.items():
                    if len(triplet) == 3:
                              row = self.getRow(i)
                              inds = sorted(self.strToIntList(indices))
                              changed = False
                              for ind in inds:
                                   if not set(row[ind].possible) <= set(triplet):
                                        row[ind].possible = list(set(row[ind].possible) & set(triplet))
                                        changed = True
                              if changed:
                                   actions.append(f"Hidden Triple: Cells {inds[0]+1},{inds[1]+1},{inds[2]+1} in row {i+1} can only be {sorted(self.strToIntList(triplet))}, removing those candidates from the row")
          for i in range(0,9):
               colP = self.getPossiblesDict(i,MODE.COLUMN,2,3)
               #{"468":[1,5,7]}
               triples = {}
               for j in range(1,10):
                    if len(colP[j]) == 3:
                         cells = self.listToStr(colP[j])
                         triples[cells] = [j]
                         for k in range(1,10):
                              if k != j and set(colP[k]) <= set(self.strToIntList(cells)):
                                   triples[cells].append(k)

               for indices, triplet in triples.items():
                    if len(triplet) == 3:
                              col = self.getCol(i)
                              inds = sorted(self.strToIntList(indices))
                              changed = False
                              for ind in inds:
                                   if not set(col[ind].possible) <= set(triplet):
                                        col[ind].possible = list(set(col[ind].possible) & set(triplet))
                                        changed = True
                              if changed:
                                   actions.append(f"Hidden Triple: Cells {inds[0]+1},{inds[1]+1},{inds[2]+1} in column {i+1} can only be {sorted(self.strToIntList(triplet))}, removing those candidates from the column")
          for i in range(0,9):
               boxP = self.getPossiblesDict(i,MODE.BOX,2,3)
               #{"468":[1,5,7]}
               triples = {}
               for j in range(1,10):
                    if len(boxP[j]) == 3:
                         cells = self.listToStr(boxP[j])
                         triples[cells] = [j]
                         for k in range(1,10):
                              if k != j and set(boxP[k]) <= set(self.strToIntList(cells)):
                                   triples[cells].append(k)

               for indices, triplet in triples.items():
                    if len(triplet) == 3:
                              box = self.getBox(i)
                              inds = sorted(self.strToIntList(indices))
                              triplet = sorted(triplet)
                              changed = False
                              for ind in inds:
                                   if not set(box[ind].possible) <= set(triplet):
                                        box[ind].possible = list(set(box[ind].possible) & set(triplet))
                                        changed = True
                              if changed:
                                   actions.append(f"Hidden Triple: Cells {inds[0]+1},{inds[1]+1},{inds[2]+1} in box {i+1} can only be {sorted(self.strToIntList(triplet))}, removing those candidates from the box")     

          return actions
     def xWing(self)-> list[str]:
          actions = []
          # by row,col, get cells that only occur twice
          # by candidate, compare indexes, if they match, block opposite using index (j = 5,8, block cols 5,8)
          totalRowP = []
          totalColP = []
          # [{1:[3,5]2:[-1]...}]
          for i in range(0,9):
               totalRowP.append(self.getPossiblesDict(i,MODE.ROW,2,2))
               totalColP.append(self.getPossiblesDict(i,MODE.COLUMN,2,2))
          for i in range(0,9):
               current = totalRowP[i]
               for j in range(1,10):
                    if current[j][0] != -1:
                         for k in range(i,9):
                              #don't compare to self
                              if k != i:
                                   if current[j] == totalRowP[k][j]:
                                        status = False
                                        for ind in current[j]:
                                             self.cells[i][ind].hasBlocked = True
                                             self.cells[k][ind].hasBlocked = True
                                             status = self.block(0,ind,j,MODE.COLUMN) or status 
                                             self.cells[i][ind].hasBlocked = False
                                             self.cells[k][ind].hasBlocked = False
                                        if status:
                                             actions.append(f"X Wing: Cells {current[j][0]+1},{current[j][1]+1} are the only cells that contain {j} in rows {i+1},{k+1}, and are in the same columns, removing the possibility of {j} in those columns.")
          for i in range(0,9):
               current = totalColP[i]
               for j in range(1,10):
                    if current[j][0] != -1:
                         for k in range(i,9):
                              #don't compare to self
                              if k != i:
                                   if current[j] == totalColP[k][j]:
                                        status = False
                                        for ind in current[j]:
                                             self.cells[ind][i].hasBlocked = True
                                             self.cells[ind][k].hasBlocked = True
                                             status = self.block(ind,0,j,MODE.ROW) or status
                                             self.cells[ind][i].hasBlocked = False
                                             self.cells[ind][k].hasBlocked = False
                                        if status:
                                             actions.append(f"X Wing: Cells {current[j][0]+1},{current[j][1]+1} are the only cells that contain {j} in columns {i+1},{k+1}, and are in the same rows, removing the possibility of {j} in those rows.")
          return actions
     def chuteRemotePairs(self)-> list[str]:
          #look by chute, get cells with only 2 candidates
          # compare cells in chute, make sure not naked pair (not in same col,row,box)
          #  get cells that can't see the pair in the remaining box of chute
          #   if they have only one of the candidates in the pair, eliminate that candidate from cells that both of the pair can see
          actions = []
          #chute
          for i in range(0,3):
               pairs = {}
               #row
               for j in range(0,3):
                    pairs[j] = {}
                    rowP = self.getPossibles(MODE.ROW,i*3+j)
                    #cell
                    for k in range(0,9):
                         if len(rowP[k]) == 2:
                              #pairs={0:{"47":[7],"68":[2]},1:{"78":[1]}}
                              if not self.listToStr(sorted(rowP[k])) in pairs[j]: 
                                   pairs[j][self.listToStr(sorted(rowP[k]))] = []
                              pairs[j][self.listToStr(sorted(rowP[k]))].append(k) 
                              
               #find any pairs that occur in 2 rows in the chute
               matches = {}
               for j in range(0,2):
                    rowPair = pairs[j]
                    for pair, indices in rowPair.items():
                         for index in indices:
                              for k in range(j+1,3):
                                   nextRowPair = pairs[k]
                                   if pair in nextRowPair:
                                             for nextIndex in nextRowPair[pair]:
                                                  # matching pair in different rows, not in same box
                                                  if math.floor(index / 3) != math.floor(nextIndex/3):
                                                       if not pair in matches:
                                                            matches[pair] = []
                                                       matches[pair].append(((j,index), (k,nextIndex)))

               #{"47":[((0,7)(1,1)),((1,3),(2,9))]}
               for match, pairCoords in matches.items():
                    for coords in pairCoords:
                         #row index relative to chute and therefore also relative to box
                         unoccupiedRowRelativeIndex = list(set([0,1,2]) - set([coords[0][0], coords[1][0]]))[0]
                         #absolute box index
                         unoccupiedBoxIndex =  i*3+list(set([0,1,2]) - set([math.floor(coords[0][1]/3), math.floor(coords[1][1]/3)]))[0]

                         cells = self.getBox(unoccupiedBoxIndex)[unoccupiedRowRelativeIndex * 3:unoccupiedRowRelativeIndex * 3 + 3]
                         foundFirst = False
                         foundSecond = False
                         candidate1 = self.strToIntList(match)[0]
                         candidate2 = self.strToIntList(match)[1]
                         for cell in cells:
                              if candidate1 in cell.possible or candidate1 == cell.num:
                                   foundFirst = True
                              if candidate2 in cell.possible or candidate2 == cell.num:
                                   foundSecond = True
                         if foundFirst ^ foundSecond:
                              firstSeen = self.getVisible(i*3+coords[0][0],coords[0][1])
                              secondSeen = self.getVisible(i*3+coords[1][0],coords[1][1])
                              intersection = list(set(firstSeen) & set(secondSeen))
                              changed = False
                              if foundFirst:
                                   for coord in intersection:
                                        if candidate1 in self.cells[coord[0]][coord[1]].possible:
                                             self.cells[coord[0]][coord[1]].possible.remove(candidate1)
                                             changed = True
                                   if changed:
                                        actions.append(f"Chute Remote Pair: Cells ({coords[0][0]+i*3+1},{coords[0][1]+1}),({coords[1][0]+i*3+1},{coords[1][1]+1}) form a remote pair, and at least one of 3 cells they don't see in their chute contain {candidate1}, removing {candidate1} from the cells that both cells can see.")

                              else:
                                   for coord in intersection:
                                        if candidate2 in self.cells[coord[0]][coord[1]].possible:
                                             self.cells[coord[0]][coord[1]].possible.remove(candidate2)
                                             changed = True
                                   if changed:
                                        actions.append(f"Chute Remote Pair: Cells ({coords[0][0]+i*3+1},{coords[0][1]+1}),({coords[1][0]+i*3+1},{coords[1][1]+1}) form a remote pair, and at least one of 3 cells they don't see in their chute contain {candidate2}, removing {candidate2} from the cells that both cells can see.")
                         #double elimination
                         elif not foundFirst and not foundSecond:
                              firstSeen = self.getVisible(i*3+coords[0][0],coords[0][1])
                              secondSeen = self.getVisible(i*3+coords[1][0],coords[1][1])
                              intersection = list(set(firstSeen) & set(secondSeen))
                              changed = False
                              for coord in intersection:
                                   if candidate1 in self.cells[coord[0]][coord[1]].possible:
                                        self.cells[coord[0]][coord[1]].possible.remove(candidate1)
                                        changed = True
                                   if candidate2 in self.cells[coord[0]][coord[1]].possible:
                                        self.cells[coord[0]][coord[1]].possible.remove(candidate2)
                                        changed = True
                              if changed:
                                   actions.append(f"Chute Remote Pair Double Elimination: Cells ({coords[0][0]+i*3+1},{coords[0][1]+1}),({coords[1][0]+i*3+1},{coords[1][1]+1}) form a remote pair, and none of 3 cells they don't see in their chute contain either {candidate1} or {candidate2}, removing {candidate1} and {candidate2} from the cells that both cells can see.")
          #chute
          for i in range(0,3):
               pairs = {}
               #col
               for j in range(0,3):
                    pairs[j] = {}
                    colP = self.getPossibles(MODE.COLUMN,i*3+j)
                    #cell
                    for k in range(0,9):
                         if len(colP[k]) == 2:
                              if not self.listToStr(sorted(colP[k])) in pairs[j]: 
                                   pairs[j][self.listToStr(sorted(colP[k]))] = []
                              pairs[j][self.listToStr(sorted(colP[k]))].append(k) 
               #find any pairs that occur in 2 rows in the chute
               matches = {}
               for j in range(0,2):
                    colPair = pairs[j]
                    for pair, indices in colPair.items():
                         for index in indices:
                              for k in range(j+1,3):
                                   nextColPair = pairs[k]
                                   if pair in nextColPair:
                                             for nextIndex in nextColPair[pair]:
                                                  # matching pair in different cols, not in same box
                                                  if math.floor(index / 3) != math.floor(nextIndex/3):
                                                       if not pair in matches:
                                                            matches[pair] = []
                                                       matches[pair].append(((index,j), (nextIndex,k)))
              
               #{"28":((5,1)(2,2))}
               for match, pairCoords in matches.items():
                    for coords in pairCoords:
                         #col index relative to chute and therefore also relative to box
                         unoccupiedColRelativeIndex = list(set([0,1,2]) - set([coords[0][1], coords[1][1]]))[0]
                         #absolute box index
                         unoccupiedBoxIndex = i + list(set([0,1,2]) - set([math.floor(coords[0][0]/3), math.floor(coords[1][0]/3)]))[0] * 3

                         cells = self.getBox(unoccupiedBoxIndex)[unoccupiedColRelativeIndex:unoccupiedColRelativeIndex+7:3]
                         foundFirst = False
                         foundSecond = False
                         candidate1 = self.strToIntList(match)[0]
                         candidate2 = self.strToIntList(match)[1]
                         for cell in cells:
                              if candidate1 in cell.possible or candidate1 == cell.num:
                                   foundFirst = True
                              if candidate2 in cell.possible or candidate2 == cell.num:
                                   foundSecond = True
                         if foundFirst ^ foundSecond:
                              firstSeen = self.getVisible(coords[0][0],i*3+coords[0][1])
                              secondSeen = self.getVisible(coords[1][0],i*3+coords[1][1])
                              intersection = list(set(firstSeen) & set(secondSeen))
                              changed = False
                              if foundFirst:
                                   for coord in intersection:
                                        if candidate1 in self.cells[coord[0]][coord[1]].possible:
                                             self.cells[coord[0]][coord[1]].possible.remove(candidate1)
                                             changed = True
                                   if changed:
                                        actions.append(f"Chute Remote Pair: Cells ({coords[0][0]+1},{coords[0][1]+i*3+1}),({coords[1][0]+1},{coords[1][1]+i*3+1}) form a remote pair, and at least one of 3 cells they don't see in their chute contain {candidate1}, removing {candidate1} from the cells that both cells can see.")

                              else:
                                   for coord in intersection:
                                        if candidate2 in self.cells[coord[0]][coord[1]].possible:
                                             self.cells[coord[0]][coord[1]].possible.remove(candidate2)
                                             changed = True
                                   if changed:
                                        actions.append(f"Chute Remote Pair: Cells ({coords[0][0]+1},{coords[0][1]+i*3+1}),({coords[1][0]+1},{coords[1][1]+i*3+1}) form a remote pair, and at least one of 3 cells they don't see in their chute contain {candidate2}, removing {candidate2} from the cells that both cells can see.")
                         #double elimination
                         elif not foundFirst and not foundSecond:
                              firstSeen = self.getVisible(coords[0][0],i*3+coords[0][1])
                              secondSeen = self.getVisible(coords[1][0],i*3+coords[1][1])
                              intersection = list(set(firstSeen) & set(secondSeen))
                              changed = False
                              for coord in intersection:
                                   if candidate1 in self.cells[coord[0]][coord[1]].possible:
                                        self.cells[coord[0]][coord[1]].possible.remove(candidate1)
                                        changed = True
                                   if candidate2 in self.cells[coord[0]][coord[1]].possible:
                                        self.cells[coord[0]][coord[1]].possible.remove(candidate2)
                                        changed = True
                              if changed:
                                   actions.append(f"Chute Remote Pair Double Elimination: Cells ({coords[0][0]+1},{coords[0][1]+i*3+1}),({coords[1][0]+1},{coords[1][1]+i*3+1}) form a remote pair, and none of 3 cells they don't see in their chute contain either {candidate1} or {candidate2}, removing {candidate1} and {candidate2} from the cells that both cells can see.")
          
          return actions
     def yWing(self) -> list[str]:
          actions = []
          for i in range(0,9):
               for j in range(0,9):
                    if len(self.cells[i][j].possible) == 2:
                         abCell = self.cells[i][j]
                         a = abCell.possible[0]
                         b = abCell.possible[1]
                         #cells that have only 2 candidates, share at most one candidate with, and are visible to ab cell
                         visibleCoords = self.getVisible(i,j)
                         possibleCells = list(filter(lambda c: len(c.possible) == 2 and ((a in c.possible) ^ (b in c.possible)),map(lambda c: self.cells[c[0]][c[1]], visibleCoords)))
                         possibleCoords = list(map( lambda c2: (c2.i,c2.j),possibleCells))
                         for cell in possibleCells:
                              acCell = None
                              bcCell = None
                              if a in cell.possible:
                                   acCell = cell
                                   c = list(set(acCell.possible) - set(abCell.possible))[0]
                                   acVisibleCoords = self.getVisible(acCell.i,acCell.j)
                                   bcPossibleCoords = set(possibleCoords) - set(acVisibleCoords)
                                   # cells that are visible to abCell but not visible to acCell, that have b and c as candidates
                                   bcPossibleCells = list(filter(lambda c1: b in c1.possible and c in c1.possible, map(lambda coord: self.cells[coord[0]][coord[1]],bcPossibleCoords)))
                                   for bc in bcPossibleCells:
                                        bcCell = bc
                                        status = False
                                        affected = list(set(self.getVisible(bcCell.i,bcCell.j)) & set(acVisibleCoords))
                                        removed = [] 
                                        for coord in affected:
                                             if c in self.cells[coord[0]][coord[1]].possible:
                                                  self.cells[coord[0]][coord[1]].possible.remove(c)
                                                  removed.append((coord[0]+1,coord[1]+1))
                                                  status = True
                                        if status:
                                             
                                             actions.append(f"Y Wing: AB Cell at {i+1},{j+1} sees AC cell {acCell.i+1},{acCell.j+1} and BC cell {bcCell.i+1},{bcCell.j+1}, removing C ({c}) from cells that can be seen by both AC and BC cells: {removed}.")
                              else:
                                   bcCell = cell
                                   c = list(set(bcCell.possible) - set(abCell.possible))[0]
                                   bcVisibleCoords = self.getVisible(bcCell.i,bcCell.j)
                                   acPossibleCoords = set(possibleCoords) - set(bcVisibleCoords)
                                   # cells that are visible to abCell but not visible to acCell, that have b and c as candidates
                                   acPossibleCells = list(filter(lambda c1: a in c1.possible and c in c1.possible, map(lambda coord: self.cells[coord[0]][coord[1]],acPossibleCoords)))
                                   for ac in acPossibleCells:
                                        acCell = ac
                                        status = False
                                        affected = list(set(self.getVisible(acCell.i,acCell.j)) & set(bcVisibleCoords)) 
                                        removed = []
                                        for coord in affected:
                                             if c in self.cells[coord[0]][coord[1]].possible:
                                                  self.cells[coord[0]][coord[1]].possible.remove(c)
                                                  removed.append((coord[0]+1,coord[1]+1))
                                                  status = True
                                        if status:
                                             actions.append(f"Y Wing: AB Cell at {i+1},{j+1} sees AC cell {acCell.i+1},{acCell.j+1} and BC cell {bcCell.i+1},{bcCell.j+1}, removing C ({c}) from cells that can be seen by both AC and BC cells: {removed}.")
          return actions
                              



                    

     # def simpleColoring(self)-> list[str]:
          # actions = []
          # for i in range(0,9):
          #      for j in range(0,9):
          #           parentCell = self.cells[i][j]
          #           if parentCell.num == -1:
          #                parentCell.on = True
          #                state = False
          #                for candidate in parentCell.possible:
          #                     visible = self.getVisible(i,j)
          #                     for coord in visible:
          #                          visibleCell = self.cells[coord[0]][coord[1]]
          #                          if candidate in visibleCell.possible:
          #                               candidate
                              
                                   


          
     def blockAll(self) -> list[str]:
          """Iterates over board, calling self.block() on any cells that haven't blocked yet and have a value"""
          actions = []
          for i in range(0,9):
               for j in range(0,9):
                    cell = self.cells[i][j]
                    if cell.num > 0 and not cell.hasBlocked:
                         c1 = self.block(i,j,cell.num, MODE.BOX)
                         c2 = self.block(i,j,cell.num, MODE.COLUMN)
                         c3 = self.block(i,j,cell.num, MODE.ROW)
                         changed = c1 or c2 or c3
                         cell.hasBlocked = True
                         if changed:
                              actions.append(f"Blocking: cell at {i+1},{j+1} blocked {cell.num}")
          return actions         
     def block(self, i, j, num, mode:MODE) -> bool:
          """Removes the input num from the list of possible numbers in the column, row, and box of the input coordinate"""
          
          changed = False
          match mode:
               case MODE.ROW:
                    r = self.getRow(i)
                    for k in range(0,9):
                         if not r[k].hasBlocked and num in r[k].possible:
                              r[k].possible.remove(num)
                              changed = True
               case MODE.COLUMN:
                    c = self.getCol(j)
                    for k in range(0,9):
                         if not c[k].hasBlocked and num in c[k].possible:
                              c[k].possible.remove(num)
                              changed = True
               case MODE.BOX:
                    b = self.getBoxFromPos(i,j)
                    for k in range(0,9):
                         if not b[k].hasBlocked and num in b[k].possible:
                              b[k].possible.remove(num)
                              changed = True
          #print(f"Blocking {num} at {i,j}, in {mode.name}, changed: {changed}")
          return changed
     def blockMultiple(self, i, j, nums:list[int], mode:MODE) -> bool:
          """Removes the input nums from the list of possible numbers in the column, row, and box of the input coordinate"""
          ret = []
          for n in nums:
               ret.append(self.block(i,j,n,mode))
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
     def getBoxIndexFromPos(self,i,j) -> int:
          i = math.floor(i / 3)
          j = math.floor(j / 3)
          return (3 * i) + j
     def updateSudoku(self, cells:list[list[Cell]]) -> None:
          self.cells = cells
     def getPossibles(self,mode:MODE, index=-1 ) -> list[list[int]]:
          ret = []
          match mode:
               case MODE.ROW:
                    for i in range(0,9):
                         ret.append(self.cells[index][i].possible)
               case MODE.COLUMN:
                    for i in range(0,9):
                         ret.append(self.cells[i][index].possible)
               case MODE.BOX:
                    box = self.getBox(index)
                    for c in box:
                         ret.append(c.possible)
               case MODE.ALL:
                    for i in range(0,9):
                         ret.append([])
                         for j in range(0,9):
                              ret[i].append(self.cells[i][j].possible)

          return ret
     def boxRelativeToAbsoluteCoords(self, boxIndex:int, cellIndex:int) -> tuple[int,int]:
          return (math.floor(boxIndex / 3) * 3 + (math.floor(cellIndex/3)),(boxIndex % 3) * 3 + (cellIndex % 3))
     def getPossiblesDict(self, index, mode:MODE,min = 0, max=9) -> dict[int:list[int]]:
          """Returns a dictionary, with the key representing the candidate, and the value a list of indices for cells that have that candidate."""
          possibles = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
          match mode:
               case MODE.ROW:
                    row = self.getRow(index)
                    for j in range(0,9):
                         for k in range(1,10):
                              #skip if cell has a value
                              if -1 in row[j].possible:
                                   break
                              elif k in row[j].possible:
                                   possibles[k].append(j)
               case MODE.COLUMN:
                    col = self.getCol(index)
                    for j in range(0,9):
                         for k in range(1,10):
                              #skip if cell has a value
                              if -1 in col[j].possible:
                                   break
                              elif k in col[j].possible:
                                   possibles[k].append(j)
               case MODE.BOX:
                    box = self.getBox(index)
                    for j in range(0,9):
                         for k in range(1,10):
                              #skip if cell has a value
                              if -1 in box[j].possible:
                                   break
                              elif k in box[j].possible:
                                   possibles[k].append(j)
               case _:
                    raise ValueError("Invalid MODE supplied to getPossiblesDict, must be MODE.ROW,MODE.COLUMN, or MODE.BOX")     
          #enforce bounds on number of cells with candidates we are looking for
          for i in range(1,10):
               if len(possibles[i]) < min or len(possibles[i]) > max:
                    possibles[i] = [-1]          
          return possibles
     def getNGroup(self, possibilities:dict[int:list[int]], candidateN:int, indexN:int) -> list[tuple[int,list[int]]]:
          """Returns a list that contains groups of n candidates that have n cells in commmon: n=2 will look for 2 candidates that have 2 cells in common, """
          pos = possibilities.copy()
          ret = []
          for i in range(1,8):
               if -1 in pos[i]: 
                    continue
               indices = set(pos[i])
               candidates = [i]
               for j in range(i+1,10):
                    #matching pair of indices
                    if not -1 in pos[i] and pos[i] == pos[j]:
                         for index in pos[j]:
                              indices.add(index)
                         candidates.append(j)
               if len(candidates) == candidateN and len(indices) == indexN:
                    ret.append((candidates,list(indices)))
          return ret     
     def getVisible(self, i:int, j:int) -> list[tuple[int,int]]:
          """Returns a list of coordinates of cells that can be seen by the cell at i,j"""
          ret = []
          #row
          for k in range(0,9):
               if k != j:
                    ret.append((i,k))
          #col
          for k in range(0,9):
               if k != i:
                    ret.append((k,j))
          boxIndex = self.getBoxIndexFromPos(i,j)
          #box
          for k in range(0,9):
               i1,j1 = self.boxRelativeToAbsoluteCoords(boxIndex,k)
               if i != i1 and j != j1:
                    ret.append((i1,j1))
          return ret
     def listToStr(self, list:list[int]) -> str:
          ret = ""
          for l in list:
               ret+=str(l)
          return ret
     def strToIntList(self, str:str) -> list[int]:
          ret = []
          nums = list(str)
          for num in nums:
               ret.append(int(num))
          return ret




