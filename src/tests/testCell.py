import unittest
from cell import Cell
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
          c1 = Cell((0,0),(0,0))
          c1.setNum(5)
          c1.drawNum(self.canvas)
          self.assertEqual(c1.textIDs["main"], 1)
          self.assertListEqual(c1.possible,[-1])
     def testDrawNoNum(self):
          c2 = Cell((1,1),(1,1))
          c2.drawNum(self.canvas)
          self.assertIsNone(c2.textIDs["main"])
          self.assertListEqual(c2.possible,[1,2,3,4,5,6,7,8,9])
     def testEraseNum(self):
          c3 = Cell((2,2),(2,2))
          c3.num = 5
          c3.drawNum(self.canvas)
          self.assertEqual(c3.textIDs["main"], 1)
          c3.eraseNum(self.canvas)
          self.assertIsNone(c3.textIDs["main"])
     def testSetNum(self):
          c4 = Cell((3,3),(3,3))
          c4.setNum(5)
          self.assertListEqual(c4.possible,[-1])
          self.assertEqual(c4.num,5)
     def testSetNegativeOneNum(self):
          c5 = Cell((4,4),(4,4))
          c5.setNum(-1)
          self.assertListEqual(c5.possible,[1,2,3,4,5,6,7,8,9])
          self.assertEqual(c5.num,-1)

if __name__ == "__main__":
     unittest.main()