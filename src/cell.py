from enum import Enum

class LineType(Enum):
     TOP = 1
     BOTTOM = 2
     RIGHT = 3
     LEFT = 4
     NONE = 5

class Cell():
     def __init__(self, p1:tuple, p2:tuple, color:str = "black", LineTypes:list[LineType] = [LineType.NONE]):
          self.x1 = p1[0]
          self.y1 = p1[1]
          self.x2 = p2[0]
          self.y2 = p2[1]
          self.lineTypes = LineTypes
          self.color = color
          self.num = -1
          self.textID = None
          # numbers that could possibly occupy the cell
          self.hasBlocked = False
          self.possible = [1,2,3,4,5,6,7,8,9]
     def draw(self, canvas):
          if LineType.TOP in self.lineTypes:
               canvas.create_line(self.x1,self.y1,self.x2,self.y1,fill=self.color,width=4)
          else:
               canvas.create_line(self.x1,self.y1,self.x2,self.y1,fill=self.color,width=2)
          if LineType.BOTTOM in self.lineTypes:
               canvas.create_line(self.x2,self.y2,self.x1,self.y2,fill=self.color,width=4)
          else:
               canvas.create_line(self.x2,self.y2,self.x1,self.y2,fill=self.color,width=2)
          if LineType.LEFT in self.lineTypes:
               canvas.create_line(self.x1,self.y2,self.x1,self.y1,fill=self.color,width=4)
          else:
               canvas.create_line(self.x1,self.y2,self.x1,self.y1,fill=self.color,width=2)
          if LineType.RIGHT in self.lineTypes:
               canvas.create_line(self.x2,self.y1,self.x2,self.y2,fill=self.color,width=4)
          else:
               canvas.create_line(self.x2,self.y1,self.x2,self.y2,fill=self.color,width=2)
     def drawNum(self, canvas) -> None:
          if self.num != -1:
               if self.textID:
                    self.delNum(canvas)
               self.textID = canvas.create_text((self.x1 + self.x2) /2, (self.y1 + self.y2) / 2, text=f"{self.num}")
               self.possible = [-1]
          
     def delNum(self, canvas) -> None:
          if self.textID:
               canvas.delete(self.textID)
               self.textID = None
               self.possible = [1,2,3,4,5,6,7,8,9]