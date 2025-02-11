import unittest
from src.cell import Cell
class DummyCanvas():
     def __init__(self):
          return
     def create_line(self,x,y,x2,y2,fill="black",width=4):
          return
     def create_text(self,x,y,text=""):
          return 1
     def delete(self,id):
          return 
class TestCell(unittest.TestCase):
     canvas = DummyCanvas()
     def testDrawNum(self):
          cell = Cell((1,1),(2,2))
          cell.num = 5
          cell.drawNum(self.canvas)
          self.assertEqual(cell.textID, 1)
          self.assertListEqual(cell.possible,[-1])
     def testDrawNoNum(self):
          cell = Cell((1,1),(2,2))
          cell.drawNum(self.canvas)
          self.assertIsNone(cell.textID)
          self.assertNotEqual(cell.possible,[-1])
     def testDelNum(self):
          cell = Cell((1,1),(2,2))
          cell.num = 5
          cell.drawNum(self.canvas)
          self.assertEqual(cell.textID, 1)
          cell.delNum(self.canvas)
          self.assertIsNone(cell.textID)
          self.assertListEqual(cell.possible,[1,2,3,4,5,6,7,8,9])
     def testDrawNum(self):
          cell = Cell((1,1),(2,2))
          cell.setNum(5)
          self.assertListEqual(cell.possible,[-1])
          self.assertEqual(cell.num,5)

if __name__ == "__main__":
     unittest.main()