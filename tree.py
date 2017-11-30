from PyQt4.QtGui import *
from PyQt4.QtCore import *

        

class Tree:
    def __init__(self,val,val2 ,x_root ,y_root,scene,node_type):

        self.root = Node(val,val2,node_type) 
        self.x_root = x_root
        self.y_root = y_root
        self.scene = scene
        
    def print_tree(self):
        print self.x_root
        print self.y_root
        self.print_tree_hidden(self.root,self.x_root,self.y_root)
    def print_tree_hidden(self,input_node ,x  , y ):
        current_node = input_node
        print x
        print y
        if current_node.type == "e":
            self.scene.addEllipse(x,y,100,50,pen = QPen(),brush = QBrush())
        else:
            self.scene.addRect(x,y,100,50,pen = QPen(),brush = QBrush())
        print current_node.val
        text = QGraphicsTextItem(current_node.val)
        text.boundingRect()
        text.setPos(x+25,y+15)
        self.scene.addItem(text)
        total_x = len(current_node.children) * 300
        print "total_x : ",total_x
        print "-------------------"
        for i,node in enumerate(current_node.children):
            if i < len(current_node.children)/2:
                new_x = x-(total_x/2) + i*100
            elif i > len(current_node.children)/2:
                new_x = x+(total_x/2) + (i-1-(len(current_node.children)/2))*120
            else:
                new_x = x
            # print "new_x : ",new_x
            new_y = y + 80
            self.print_tree_hidden(node,new_x,new_y)
            self.scene.addLine(x + 50,y + 50,new_x + 50,new_y + 10,pen = QPen())



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
    x.root.add_child(Node("cond"," ","r"))
    x.root.add_child(Node("then"," ","e"))
    # x.root.add_child(Node("else"," ","e"))
    x.root.children[0].add_child(Node("exp"," ","e"))
    x.root.children[0].add_child(Node("op"," ","e"))
    x.print_tree()
    scene = x.scene

    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.resize(1000, 600)
    view.show()
    app.exec_()
