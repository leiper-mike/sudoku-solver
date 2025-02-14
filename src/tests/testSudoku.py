import unittest
from cell import Cell
from sudoku import Sudoku

class TestSudoku(unittest.TestCase):
     def testCheck(self):
          cells = []
          solved = [
               [5,3,4,6,7,8,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,2,5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,8,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9],
          ]
          for i in range(0,9):
               cells.append([])
               for j in range(0,9):
                    cells[i].append(Cell((0,0),(0,0)))
                    cells[i][j].num = solved[i][j]
          sudoku = Sudoku(cells)
          status = sudoku.check()
          self.assertTrue(status)
     def testCheckFail(self):
          cells = []
          solved = [
               [5,3,4,6,8,7,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,2,5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,8,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9],
          ]
          for i in range(0,9):
               cells.append([])
               for j in range(0,9):
                    cells[i].append(Cell((0,0),(0,0)))
                    cells[i][j].num = solved[i][j]
          sudoku = Sudoku(cells)
          status = sudoku.check()
          self.assertFalse(status)
     def testCheckEmpty(self):
          cells = []
          solved = [
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
          ]
          for i in range(0,9):
               cells.append([])
               for j in range(0,9):
                    cells[i].append(Cell((0,0),(0,0)))
                    cells[i][j].num = solved[i][j]
          sudoku = Sudoku(cells)
          status = sudoku.check()
          self.assertFalse(status)
     def testNakedSingle(self):
          input = [
               [[1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[2]  ],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[3],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[4]  ],
          ]
          correct = [
               "Naked Single: Cell at Row: 1, Column: 1 set to 1",
               "Naked Single: Cell at Row: 1, Column: 9 set to 2",
               "Naked Single: Cell at Row: 9, Column: 1 set to 3",
               "Naked Single: Cell at Row: 9, Column: 9 set to 4"
               ]
          cells = cellPossibleFromNums(input)
          sudoku = Sudoku(cells)
          status = sudoku.nakedSingle()
          self.assertListEqual(status,correct)
          self.assertEqual(sudoku.cells[0][0].num, 1)
          self.assertEqual(sudoku.cells[0][8].num, 2)
          self.assertEqual(sudoku.cells[8][0].num, 3)
          self.assertEqual(sudoku.cells[8][8].num, 4)
     def testHiddenSingle(self):
          input = [
               [[-1],[-1],[-1],[-1],[7],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[6],[-1],[-1],[-1],[-1]],
               [[-1],[2,9],[2,9],[4,5],[-1],[4,5],[-1],[-1],[-1]],
               [[-1],[-1],[4,9],[3,4,6],[3,4,6,9],[4,8,9],[6,8],[-1],[-1]],
               [[-1],[-1],[-1],[5,3],[-1],[5,7,9],[-1],[9],[3,9]],
               [[-1],[-1],[4,9],[2,4,6],[2,4,6,9],[4,8,9],[6,8],[-1],[-1]],
               [[-1],[2,6,9],[-1],[2,3],[-1],[9],[7,6],[6,9],[-1]],
               [[4,9],[5,6,9],[-1],[-1],[4,9],[-1],[-1],[5,6,9],[8,9]],
               [[4,9],[2,5,9],[-1],[-1],[2,4,9],[-1],[-1],[1,5,9],[9]],
          ]
          solved = [
               [-1,-1,-1,-1, 7,-1,-1,-1,-1],
               [-1,-1,-1,-1, 6,-1,-1,-1,-1],
               [-1,-1,2,-1,-1, 5,-1,-1,-1],
               [-1,-1,-1,-1,3,-1,-1,-1,-1],
               [-1,-1,-1,5,-1,7,-1,-1,3],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,3,-1,-1,7,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,5,8],
               [4,5,-1,-1,2,-1,-1,1,9],
          ]
          correct = [
               "Hidden Single: row #1, col#5 set to: 7",
               'Hidden Single: row #2, col#5 set to: 6',
               'Hidden Single: col#3, row #3 set to: 2',
               'Hidden Single: row #5, col#6 set to: 7',
               'Hidden Single: col#5, row #4 set to: 3',
               'Hidden Single: item#4, in box5 set to: 5',
               'Hidden Single: col#6, row #3 set to: 5',
               'Hidden Single: item#6, in box6 set to: 3',
               'Hidden Single: row #7, col#4 set to: 3',
               'Hidden Single: row #7, col#7 set to: 7',
               'Hidden Single: row #8, col#9 set to: 8',
               'Hidden Single: col#8, row #9 set to: 1',
               'Hidden Single: item#8, in box8 set to: 2',
               'Hidden Single: row #9, col#1 set to: 4',
               'Hidden Single: row #9, col#2 set to: 5',
               'Hidden Single: col#9, row #9 set to: 9',
               'Hidden Single: item#5, in box9 set to: 5'
          ]
          cells = cellPossibleFromNums(input)
          sudoku = Sudoku(cells)
          status = sudoku.hiddenSingle()
          self.assertListEqual(status,correct)
          for i in range(0,9):
               for j in range(0,9):
                     self.assertEqual(cells[i][j].num, solved[i][j], msg=f"i:{i},j{j}")
          
     def testNakedPairs(self):
          input = [
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[1,2,6,9],[1,2,8,9],[1,2,6],[1,6,7,8],[-1],[1,6,7,8],[-1],[-1],[1,8,9]],
               [[1,6],[-1],[1,6],[-1],[-1],[-1],[1,5,6,8],[-1],[1,5,8]],
               [[-1],[-1],[-1],[1,6,7,8],[-1],[1,6,7,8],[1,6,7,8],[6,7,8,9],[1,8,9]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               ]
          correct = [
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[2,9],[2,8,9],[2],[1,6,7,8],[-1],[1,6,7,8],[-1],[-1],[1,9]],
               [[1,6],[-1],[1,6],[-1],[-1],[-1],[5,8],[-1],[5,8]],
               [[-1],[-1],[-1],[1,6,7,8],[-1],[1,6,7,8],[1,6,7],[6,7,9],[1,9]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               ]
          correctStatus = [
               'Naked Pair: Cells 5,1 and 5,3, eliminating [1, 6] in row 5 and box #4',
               'Naked Pair: Cells 5,7 and 5,9, eliminating [5, 8] in row 5 and box #6'
               ]
          cells = cellPossibleFromNums(input)
          sudoku = Sudoku(cells)
          status = sudoku.nakedPairs()
          self.assertListEqual(status, correctStatus)
          for i in range(0,9):
               for j in range(0,9):
                     self.assertEqual(sudoku.cells[i][j].possible, correct[i][j], msg=f"i:{i},j{j}")
          
     def testHiddenPairs(self):
          input = [
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[1,8,9]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[5,8],[-1],[5,8]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[1,6,7,8],[6,7,8,9],[1,8,9]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               ]
          correct = [
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[1,8,9]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[5,8],[-1],[5,8]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[6,7],[6,7],[1,8,9]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
                    [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               ]
          correctStatus = [
               "Hidden pair: Cells #7,8 in box #6 are the only cells to contain both 6 and 7, therefore they must be one of the two"
               ]
          cells = cellPossibleFromNums(input)
          sudoku = Sudoku(cells)
          status = sudoku.hiddenPairs()
          self.assertListEqual(status, correctStatus)
          for i in range(0,9):
               for j in range(0,9):
                     self.assertEqual(sudoku.cells[i][j].possible, correct[i][j], msg=f"i:{i},j{j}")
     def testVirtualSingle(self):
          input = [
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],      [1,2,7],[-1],[-1],[2,7],[7,9],[2,9] ],
               [[1,2,9],[1,2,9],[-1],[1,2,8],[-1],[-1],[2,5,8],[5,8,9],[-1]],
               [[-1],[2],[-1],       [2,7,8],[8],[-1], [-1],[-1],[-1]    ],
               ]
          correct = [
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]],
               [[-1],[-1],[-1],      [1,2],[-1],[-1],  [2,7],[7,9],[2,9] ],
               [[1,2,9],[1,2,9],[-1],[2],[-1],[-1],    [2,5,8],[5,8],[-1]  ],
               [[-1],[2],[-1],       [2,7,8],[8],[-1], [-1],[-1],[-1]    ],
               ]
          correctStatus = [
               'Virtual Single: Cells 8,1 and 8,2 are the only cells that contain 1, and are in a row in box #7, removing possibilities of 1 in row 8',
               'Virtual Single: Cells 8,1 and 8,2 are the only cells that contain 9, and are in a row in box #7, removing possibilities of 9 in row 8',
               'Virtual Single: Cells 7,7 and 7,8 are the only cells that contain 7, and are in a row in box #9, removing possibilities of 7 in row 7',
               'Virtual Single: Cells 8,7 and 8,8 are the only cells that contain 8, and are in a row in box #9, removing possibilities of 8 in row 8'
               ]
          cells = cellPossibleFromNums(input)
          sudoku = Sudoku(cells)
          status = sudoku.virtualSingle()
          self.assertListEqual(status,correctStatus)
          for i in range(0,9):
               for j in range(0,9):
                     self.assertEqual(sudoku.cells[i][j].possible, correct[i][j], msg=f"i:{i},j{j}")
     def testEmptyNaive(self):
          input = [
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
          ]
          cells = cellsFromNums(input)
          sudoku = Sudoku(cells)
          output = sudoku.naive()
          self.assertListEqual(output,[])
          for i in range(0,9):
               for j in range(0,9):
                    self.assertEqual(sudoku.cells[i][j].num, -1)
                    self.assertEqual(sudoku.cells[i][j].possible, [1,2,3,4,5,6,7,8,9])
     def testGetCol(self):
          nums = [
               [5,3,4,6,8,7,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,2,5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,8,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9],
          ]
          sudoku = Sudoku(cellsFromNums(nums))
          ret = list(map(lambda c: c.num,sudoku.getCol(0)))

          self.assertListEqual(ret,[5,6,1,8,4,7,9,2,3])
     def testGetRow(self):
          nums = [
               [5,3,4,6,8,7,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,2,5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,8,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9],
          ]
          sudoku = Sudoku(cellsFromNums(nums))
          ret = list(map(lambda c: c.num,sudoku.getRow(0)))

          self.assertListEqual(ret,[5,3,4,6,8,7,9,1,2])
     def testGetBox(self):
          nums = [
               [5,3,4,6,8,7,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,2,5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,8,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9],
          ]
          sudoku = Sudoku(cellsFromNums(nums))
          ret = list(map(lambda c: c.num,sudoku.getBox(0)))

          self.assertListEqual(ret,[5,3,4,6,7,2,1,9,8])
     def testGetBoxPos(self):
          cells = []
          for i in range(0,9):
               cells.append([])
               for j in range(0,9):
                    cells[i].append(Cell((0,0),(0,0)))
          sudoku = Sudoku(cells)
          pos = sudoku.getBoxPos(0)
          self.assertTupleEqual(pos,(0,0))
          pos1 = sudoku.getBoxPos(2)
          self.assertTupleEqual(pos1,(0,6))
          pos2 = sudoku.getBoxPos(4)
          self.assertTupleEqual(pos2,(3,3))
     def testGetBoxPos(self):
          solved = [
               [5,3,4,6,8,7,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,2,5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,8,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9],
          ]
          sudoku = Sudoku(cellsFromNums(solved))
          ret = list(map(lambda c: c.num,sudoku.getBoxFromPos(3,5)))

          self.assertListEqual(ret,[7,6,1,8,5,3,9,2,4])
     def testBlockAll(self):
          nums = [
               [3,-1,5,1,-1,2,9,-1,-1],
               [-1,-1,8,9,-1,3,5,-1,-1],
               [-1,-1,-1,-1,8,-1,-1,-1,7],
               [7,1,-1,-1,-1,-1,-1,2,5],
               [-1,-1,6,-1,-1,-1,4,-1,-1],
               [5,3,-1,-1,-1,-1,-1,7,1],
               [8,-1,1,-1,5,-1,-1,-1,4],
               [-1,-1,3,7,-1,1,2,-1,-1],
               [-1,-1,7,8,-1,6,3,-1,-1]
          ]
          correct = [
               [[-1],[4,6,7],[-1],[-1],[4,6,7],[-1],[-1],[4,6,8],[6,8]],
               [[1,2,4,6],[2,4,6,7],[-1],[-1],[4,6,7],[-1],[-1],[1,4,6],[2,6]],
               [[1,2,4,6,9], [2,4,6,9], [2,4,9], [4,5,6], [-1], [4,5], [1,6], [1,3,4,6], [-1]],
               [[-1],[-1,],[4,9],[3,4,6],[3,4,6,9],[4,8,9],[6,8],[-1],[-1]],
               [[2,9],[2,8,9],[-1],[2,3,5],[1,2,3,7,9],[5,7,8,9],[-1],[3,8,9],[3,8,9]],
               [[-1],[-1],[2,4,9],[2,4,6],[2,4,6,9],[4,8,9],[6,8],[-1],[-1]],
               [[-1],[2,6,9],[-1],[2,3],[-1],[9],[6,7],[6,9],[-1]],
               [[4,6,9],[4,5,6,9],[-1],[-1],[4,9],[-1],[-1],[5,6,8,9],[6,8,9]],
               [[2,4,9],[2,4,5,9],[-1],[-1],[2,4,9],[-1],[-1],[1,5,9],[9]]
          ]
          cells = cellsFromNums(nums)
          sudoku = Sudoku(cells)
          status = sudoku.blockAll()
          self.assertTrue(status)

          possibles = sudoku.getPossibles()
          self.assertListEqual(possibles,correct)
          
     def testBlockRow(self):
          nums = [
               [3,-1,5,1,-1,2,9,-1,-1],
               [-1,-1,8,9,-1,3,5,-1,-1],
               [-1,-1,-1,-1,8,-1,-1,-1,7],
               [7,1,-1,-1,-1,-1,-1,2,5],
               [-1,-1,6,-1,-1,-1,4,-1,-1],
               [5,3,-1,-1,-1,-1,-1,7,1],
               [8,-1,1,-1,5,-1,-1,-1,4],
               [-1,-1,3,7,-1,1,2,-1,-1],
               [-1,-1,7,8,-1,6,3,-1,-1]
          ]
          correct = [
               [[-1],[1,2,4,5,6,7,8,9],[-1],[-1],[1,2,4,5,6,7,8,9],[-1],[-1],[1,2,4,5,6,7,8,9],[1,2,4,5,6,7,8,9]],

          ]
          cells = cellsFromNums(nums)
          sudoku = Sudoku(cells)
          status = sudoku.block(0,0,3,col=False,box=False)
          possibles = sudoku.getPossibles()
          self.assertListEqual(possibles[0],correct[0])
          self.assertTrue(status)
     def testBlockCol(self):
          nums = [
               [3,-1,5,1,-1,2,9,-1,-1],
               [-1,-1,8,9,-1,3,5,-1,-1],
               [-1,-1,-1,-1,8,-1,-1,-1,7],
               [7,1,-1,-1,-1,-1,-1,2,5],
               [-1,-1,6,-1,-1,-1,4,-1,-1],
               [5,3,-1,-1,-1,-1,-1,7,1],
               [8,-1,1,-1,5,-1,-1,-1,4],
               [-1,-1,3,7,-1,1,2,-1,-1],
               [-1,-1,7,8,-1,6,3,-1,-1]
          ]
          correct = [
               [[-1],[-1],[1,2,4,5,6,7,8,9],[1,2,4,5,6,7,8,9],[-1],[1,2,4,5,6,7,8,9],[-1],[-1],[-1]],

          ]
          cells = cellsFromNums(nums)
          sudoku = Sudoku(cells)
          status = sudoku.block(0,2,3,row=False,box=False)
          possibles = sudoku.getPossibles()
          self.assertListEqual(list(map(lambda p: p[2] ,possibles)),correct[0])
          self.assertTrue(status)
     def testBlockBox(self):
          nums = [
               [3,-1,5,1,-1,2,9,-1,-1],
               [-1,-1,8,9,-1,3,5,-1,-1],
               [-1,-1,-1,-1,8,-1,-1,-1,7],
               [7,1,-1,-1,-1,-1,-1,2,5],
               [-1,-1,6,-1,-1,-1,4,-1,-1],
               [5,3,-1,-1,-1,-1,-1,7,1],
               [8,-1,1,-1,5,-1,-1,-1,4],
               [-1,-1,3,7,-1,1,2,-1,-1],
               [-1,-1,7,8,-1,6,3,-1,-1]
          ]
          correct = [
               [[-1],[1,2,4,5,6,7,8,9],[-1],[1,2,4,5,6,7,8,9],[1,2,4,5,6,7,8,9],[-1],[1,2,4,5,6,7,8,9],[1,2,4,5,6,7,8,9],[1,2,4,5,6,7,8,9]],

          ]
          cells = cellsFromNums(nums)
          sudoku = Sudoku(cells)
          status = sudoku.block(0,0,3,row=False,col=False)
          possibles = list(map(lambda c: c.possible ,sudoku.getBox(0)))
          self.assertListEqual(possibles,correct[0])
          self.assertTrue(status)
          

def cellsFromNums(nums:list[list[int]]) -> list[list[Cell]]:
     cells = []
     for i in range(0,9):
          cells.append([])
          for j in range(0,9):
               cells[i].append(Cell((0,0),(0,0)))
               cells[i][j].setNum(nums[i][j])
     return cells
def cellPossibleFromNums(nums:list[list[list[int]]]) -> list[list[Cell]]:
     cells = []
     for i in range(0,9):
          cells.append([])
          for j in range(0,9):
               cells[i].append(Cell((0,0),(0,0)))
               cells[i][j].possible = nums[i][j]
     return cells
if __name__ == "__main__":
     unittest.main()