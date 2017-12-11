from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Tree:
    def __init__(self,node,x_root,y_root,scene):
        self.root = node
        self.x_root = x_root
        self.y_root = y_root
        self.scene = scene
        self.level = 0
        
    def print_tree(self,levels):
        self.level = levels
        self.print_tree_hidden(self.root,self.x_root,self.y_root)

    def get_previoud_child(self,node):
        parent = node.parent
        if parent:
            node_index = parent.children.index(node)
            if node_index == 0:
                return None
            return parent.children[node_index - 1]

    def print_tree_hidden_breadth(self,input_node):
        width = 80
        height = 50
        nodes = []
        stack = [input_node]
        y = 50
        x = 50
        last_depth = 0
        while stack:
            current_node  = stack[0]
            if current_node.depth > last_depth:
                last_depth = current_node.depth
                x = 50
            if current_node.print_node:
                y = height*2* (current_node.depth + 1)
                if current_node.parent.x - 50 > x:
                    x = current_node.parent.x - 50
                current_node.x = x
                current_node.y = y
                if current_node.type == "e":
                    self.scene.addEllipse(x,y,width,height,pen = QPen(),brush = QBrush())
                else:
                    self.scene.addRect(x,y,width,height,pen = QPen(),brush = QBrush())
                previous_child = self.get_previoud_child(current_node)
                if previous_child:
                    if previous_child.type == "r" and current_node.type == "r":
                        self.scene.addLine(previous_child.x + width,previous_child.y + height/2,x ,y+height/2,pen = QPen())
                if current_node.connect:
                    self.scene.addLine(current_node.parent.x+width/2,current_node.parent.y+height,current_node.x + width/2,current_node.y,pen = QPen())
                if current_node.type == "r" and current_node.depth != 1 :
                    if previous_child:
                        if previous_child.type != "r":
                            self.scene.addLine(current_node.parent.x+width/2,current_node.parent.y+height,current_node.x + width/2,current_node.y,pen = QPen())
                    else:
                        self.scene.addLine(current_node.parent.x+width/2,current_node.parent.y+height,current_node.x + width/2,current_node.y,pen = QPen())
                font = QFont()
                font.setPixelSize(10)
                text = QGraphicsTextItem(str(current_node.val))
                text2 = QGraphicsTextItem(str(current_node.val2))
                text.setFont(font)
                text.boundingRect()
                text.setPos(x+width/3.5,y+height/4)
                text2.setFont(font)
                text2.boundingRect()
                text2.setPos(x+(width/3),y+height/4 + 15)
                self.scene.addItem(text)
                self.scene.addItem(text2)
                x = x + width + 30
            stack = stack[1:]
            nodes.append(current_node)
            for child in current_node.children:
                child.parent = current_node
                child.depth = current_node.depth + 1
                stack.append(child)

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
        self.depth = 0
        self.parent = None
        self.x = 0
        self.y = 0
    def add_child(self,node):
        self.children.append(node)

