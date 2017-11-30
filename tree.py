from PyQt4.QtGui import *
from PyQt4.QtCore import *

old_x = 0

class Tree:
    def __init__(self,val,val2 ,x_root ,y_root,scene,node_type):

        self.root = Node(val,val2,node_type) 
        self.x_root = x_root
        self.y_root = y_root
        self.scene = scene
        self.level = 0
        
    def print_tree(self,levels):
        self.level = levels
        self.print_tree_hidden(self.root,self.x_root,self.y_root)
    def print_tree_hidden(self,input_node ,x  , y ):
        self.level -= 2
        current_node = input_node
        if current_node.type == "e":
            self.scene.addEllipse(x,y,100,50,pen = QPen(),brush = QBrush())
        else:
            self.scene.addRect(x,y,100,50,pen = QPen(),brush = QBrush())
        text = QGraphicsTextItem(current_node.val)
        text.boundingRect()
        text.setPos(x+25,y+15)
        self.scene.addItem(text)
        total_x = len(current_node.children) * 100 * self.level
        for i,node in enumerate(current_node.children):
            margin = (total_x - (len(current_node.children)*100))/(len(current_node.children))
            if i < len(current_node.children)/2:
                new_x = x-(total_x/2) + (i) * (margin + 100)
            elif i >= len(current_node.children)/2:
                new_x = x-(total_x/2) + (i) * (margin + 100)
            else:
                new_x = x
            new_y = y + 150
            self.print_tree_hidden(node,new_x,new_y)
            self.scene.addLine(x + 50,y + 50,new_x + 50,new_y,pen = QPen())
            self.level += 2



class Node:
    def __init__(self,val,val2,node_type):
        self.val = val
        self.val2 = val2 
        self.type = node_type
        self.children = []
    def add_child(self,node):
        self.children.append(node)

if __name__ == "__main__":
    app = QApplication([])
    scene = QGraphicsScene()
    x = Tree(val = "if",val2 = " ",x_root = 500,y_root = 500,scene= scene,node_type="r")
    x.root.add_child(Node("cond"," ","e"))
    x.root.add_child(Node("then"," ","e"))
    x.root.add_child(Node("else"," ","e"))
    x.root.children[0].add_child(Node("exp"," ","e"))
    x.root.children[0].add_child(Node("op"," ","e"))
    x.root.children[1].add_child(Node("op"," ","e"))
    x.root.children[1].add_child(Node("op"," ","e"))



    x.print_tree(6)
    scene = x.scene

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.resize(1000, 600)
    view.show()
    app.exec_()
