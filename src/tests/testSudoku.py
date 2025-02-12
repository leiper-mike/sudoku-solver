import unittest
from src.sudoku import Sudoku
from src.cell import Cell
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
          cells = []
          solved = [
               [[5],[3],[4],[6],[7],[8],[9],[1],[2]],
               [[6],[7],[2],[1],[9],[5],[3],[4],[8]],
               [[1],[9],[8],[3],[4],[2],[5],[6],[7]],
               [[8],[5],[9],[7],[6],[1],[4],[2],[3]],
               [[4],[2],[6],[8],[5],[3],[7],[9],[1]],
               [[7],[1],[3],[9],[2],[4],[8],[5],[6]],
               [[9],[6],[1],[5],[3],[7],[2],[8],[4]],
               [[2],[8],[7],[4],[1],[9],[6],[3],[5]],
               [[3],[4],[5],[2],[8],[6],[1],[7],[9]],
          ]
          for i in range(0,9):
               cells.append([])
               for j in range(0,9):
                    cells[i].append(Cell((0,0),(0,0)))
                    cells[i][j].possible = solved[i][j]
          sudoku = Sudoku(cells)
          status = sudoku.nakedPairs()
          #self.assertFalse(status)
          for i in range(0,9):
               for j in range(0,9):
                    cells[i][j].num = solved[i][j][0]
                    self.assertEqual(cells[i][j].num, sudoku.cells[i][j].num)
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
               [-1,-1,-1,-1,-1,7,-1,-1,3],
               [-1,-1,-1,-1,-1,-1,-1,-1,-1],
               [-1,-1,-1,3,-1,-1,7,-1,-1],
               [-1,-1,-1,-1,-1,-1,-1,5,8],
               [4,5,-1,-1,2,-1,-1,1,9],
          ]
          cells = cellPossibleFromNums(input)
          sudoku = Sudoku(cells)
          status = sudoku.hiddenSingle()
          self.assertTrue(status)
          for i in range(0,9):
               for j in range(0,9):
                     self.assertEqual(cells[i][j].num, solved[i][j], msg=f"i:{i},j{j}")
          
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

          possibles = sudoku.getAllPossibles()
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
          possibles = sudoku.getAllPossibles()
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
          possibles = sudoku.getAllPossibles()
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