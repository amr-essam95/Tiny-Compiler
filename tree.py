from PyQt4.QtGui import *
from PyQt4.QtCore import *

old_x = 0

class Tree:
    # def __init__(self,val,val2 ,x_root ,y_root,scene,node_type):
    def __init__(self,node,x_root,y_root,scene):
        # self.root = Node(val,val2,node_type,False,False) 
        self.root = node
        self.x_root = x_root
        self.y_root = y_root
        self.scene = scene
        self.level = 0
        
    def print_tree(self,levels):
        self.level = levels
        self.print_tree_hidden(self.root,self.x_root,self.y_root)

    def print_tree_hidden_breadth(self,input_node,x,y):
        nodes = []
        stack = [input_node]
        while stack:
            current_node  = stack[0]
            if current_node.print_node:
                if current_node.type == "e":
                    self.scene.addEllipse(x,y,50,25,pen = QPen(),brush = QBrush())
                else:
                    self.scene.addRect(x,y,50,25,pen = QPen(),brush = QBrush())
                font = QFont()
                font.setPixelSize(10)
                text = QGraphicsTextItem(str(current_node.val)+"\n"+str(current_node.val2))
                text.setFont(font)
                text.boundingRect()
                text.setPos(x+5,y+1)
                self.scene.addItem(text)
            stack = stack[1:]
            nodes.append(current_node)
            for child in current_node.children:
                stack.append(child)


        self.level -= 1
        current_node = input_node
        if current_node.print_node:
            if current_node.type == "e":
                self.scene.addEllipse(x,y,50,25,pen = QPen(),brush = QBrush())
            else:
                self.scene.addRect(x,y,50,25,pen = QPen(),brush = QBrush())
            font = QFont()
            font.setPixelSize(10)
            text = QGraphicsTextItem(str(current_node.val)+"\n"+str(current_node.val2))
            text.setFont(font)
            text.boundingRect()
            text.setPos(x+5,y+1)
            self.scene.addItem(text)
        total_x = len(current_node.children) * 100 * self.level
        print "t ",total_x
        for i,node in enumerate(current_node.children):
            margin = (total_x - (len(current_node.children)*100))/(len(current_node.children))
            print "m ",margin
            if i < len(current_node.children)/2:
                new_x = x-(total_x/2) + (i) * (margin + 100)
                print "new_x : ",new_x
            elif i > len(current_node.children)/2:
                new_x = x-(total_x/2) + (i) * (margin + 100)
                print "new_x : ",new_x
            else:
                new_x = x
            new_y = y + 150
            self.print_tree_hidden(node,new_x,new_y)
            if node.connect:
                self.scene.addLine(x + 25,y + 25,new_x + 25,new_y,pen = QPen())
            self.level += 1
    def print_tree_hidden(self,input_node ,x ,y):
        self.level -= 1
        current_node = input_node
        if current_node.print_node:
            if current_node.type == "e":
                self.scene.addEllipse(x,y,50,25,pen = QPen(),brush = QBrush())
            else:
                self.scene.addRect(x,y,50,25,pen = QPen(),brush = QBrush())
            font = QFont()
            font.setPixelSize(10)
            text = QGraphicsTextItem(str(current_node.val)+"\n"+str(current_node.val2))
            text.setFont(font)
            text.boundingRect()
            text.setPos(x+5,y+1)
            self.scene.addItem(text)
        total_x = len(current_node.children) * 100 * self.level
        print "t ",total_x
        for i,node in enumerate(current_node.children):
            margin = (total_x - (len(current_node.children)*100))/(len(current_node.children))
            print "m ",margin
            if i < len(current_node.children)/2:
                new_x = x-(total_x/2) + (i) * (margin + 100)
                print "new_x : ",new_x
            elif i > len(current_node.children)/2:
                new_x = x-(total_x/2) + (i) * (margin + 100)
                print "new_x : ",new_x
            else:
                new_x = x
            new_y = y + 150
            self.print_tree_hidden(node,new_x,new_y)
            if node.connect:
                self.scene.addLine(x + 25,y + 25,new_x + 25,new_y,pen = QPen())
            self.level += 1
            # print "%s\n\n"%current_node.val
    def get_levels(self,node):
        max = 0
        for child in node.children:
            l = self.get_levels(child)
            if l > max:
                max = l
        return max + 1


class Node:
    def __init__(self,val,val2,node_type,print_node,connect):
        self.val = val
        self.val2 = val2 
        self.type = node_type
        self.children = []
        self.print_node =  print_node
        self.connect = connect
    def add_child(self,node):
        self.children.append(node)

if __name__ == "__main__":
    app = QApplication([])
    scene = QGraphicsScene()
    x = Tree(val = "if",val2 = " ",x_root = 500,y_root = 500,scene= scene,node_type="r")
    x.root.add_child(Node("read"," ","r",True,False))
    x.root.add_child(Node("if"," ","r",True,False))
    # x.root.add_child(Node("else"," ","e",True))
    # x.root.children[0].add_child(Node("exp"," ","e",True))
    # x.root.children[0].add_child(Node("op"," ","e",True))
    x.root.children[1].add_child(Node("op"," ","e",True,True))
    x.root.children[1].add_child(Node("assign"," ","r",True,True))
    x.root.children[1].children[0].add_child(Node("const"," ","e",True,True))
    x.root.children[1].children[0].add_child(Node("id"," ","e",True,True))
    x.root.children[1].add_child(Node("repeat"," ","r",True,False))
    x.root.children[1].add_child(Node("write"," ","r",True,False))



    x.print_tree(6)
    scene = x.scene

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.resize(1000, 600)
    view.show()
    app.exec_()
