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
          # numbers that could possibly occupy the cell
          self.hasBlocked = False
          self.possible = [1,2,3,4,5,6,7,8,9]
          self.textIDs = {"main":None,1:None,2:None,3:None,4:None,5:None,6:None,7:None,8:None,9:None}
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
          """Draws the number of the cell on the canvas, replaces current number text, erases candidate text"""
          if self.num != -1:
               if self.textIDs["main"]:
                    self.eraseNum(canvas)
               self.textIDs["main"] = canvas.create_text((self.x1 + self.x2) /2, (self.y1 + self.y2) / 2, text=f"{self.num}")
               self.erasePossible(canvas)
               
          
     def delNum(self) -> None:
          """Resets the number, and it's candidates"""
          self.num = -1
          self.possible = [1,2,3,4,5,6,7,8,9]

     def eraseNum(self,canvas):
          """Deletes the number text from the canvas"""
          if self.textIDs["main"]:
               canvas.delete(self.textIDs["main"])
               self.textIDs["main"] = None
     
     def erasePossible(self,canvas,num = 0):
          """Deletes the candidates text from the canvas"""
          if not num:
               for i in range(1,10):
                    self.erasePossible(canvas, i)
          elif self.textIDs[num]:
               canvas.delete(self.textIDs[num])
               self.textIDs[num] = None

     def setNum(self,num):
          """Sets the num variable equal to num, and removes all possibilities. If -1 is inputted, deletes number variable"""
          if num != -1:
               self.num = num
               self.possible = [-1]
          else:
               self.delNum()
               
     def drawPossible(self,canvas):
          """Draws candidate text on the canvas"""
          if not -1 in self.possible:
               for num in self.possible:
                    match num:
                         case 1:
                              if self.textIDs[1]:
                                   self.erasePossible(canvas,1)
                              self.textIDs[1] = canvas.create_text(self.x1+5, self.y1+8, text=f"{num}", font=("TkTextFont", 7))
                         case 2:
                              if self.textIDs[2]:
                                   self.erasePossible(canvas,2)
                              self.textIDs[2] = canvas.create_text(self.x1+12, self.y1+8, text=f"{num}", font=("TkTextFont", 7))
                         case 3:
                              if self.textIDs[3]:
                                   self.erasePossible(canvas,3)
                              self.textIDs[3] = canvas.create_text(self.x1+19, self.y1+8, text=f"{num}", font=("TkTextFont", 7))
                         case 4:
                              if self.textIDs[4]:
                                   self.erasePossible(canvas,4)
                              self.textIDs[4] = canvas.create_text(self.x1+5, self.y1+16, text=f"{num}", font=("TkTextFont", 7))
                         case 5:
                              if self.textIDs[5]:
                                   self.erasePossible(canvas,5)
                              self.textIDs[5] = canvas.create_text(self.x1+12, self.y1+16, text=f"{num}", font=("TkTextFont", 7))
                         case 6:
                              if self.textIDs[6]:
                                   self.erasePossible(canvas,6)
                              self.textIDs[6] = canvas.create_text(self.x1+19, self.y1+16, text=f"{num}", font=("TkTextFont", 7))
                         case 7:
                              if self.textIDs[7]:
                                   self.erasePossible(canvas,7)
                              self.textIDs[7] = canvas.create_text(self.x1+5, self.y1+24, text=f"{num}", font=("TkTextFont", 7))
                         case 8:
                              if self.textIDs[8]:
                                   self.erasePossible(canvas,8)
                              self.textIDs[8] = canvas.create_text(self.x1+12, self.y1+24, text=f"{num}", font=("TkTextFont", 7))
                         case 9:
                              if self.textIDs[9]:
                                   self.erasePossible(canvas,9)
                              self.textIDs[9] = canvas.create_text(self.x1+19, self.y1+24, text=f"{num}", font=("TkTextFont", 7))