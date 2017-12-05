import re
from pptree import *
import scanner as sc
import tree as t
from PyQt4.QtGui import *
from PyQt4.QtCore import *

app = QApplication([])
scene = QGraphicsScene()
x_root = 0
y_root = 0

class Parser(object):
	"""Parser for the Tiny Language"""
	tokens = ""
	token_index = 0

	def __init__(self):
		super(Parser, self).__init__()
		scanner = sc.Scanner()
		self.tokens = scanner.run()
		self.token_index = 0
		self.out = open('parser_output3.txt','w')
		
	def get_token(self):
		""" This function get the in order token and proceed to the next token"""
		self.token_index += 1
		return self.tokens[self.token_index - 1]

	def top_token(self):
		""" This function gets the in order token but don't proceed to the next token"""
		return self.tokens[self.token_index]

	def error(self):
		print "\n\nerror occured !!!\n\n"


	def match(self,expected_token,check_second = False):
		token = self.top_token()[0]
		if check_second:
			token = self.top_token()[1]
		if token == expected_token:	self.get_token()
		else:	self.error()

	def program(self):
		# root = t.Node("root"," ","r",True,True)
		temp = t.Node("root"," ","r",False,False)
		root = self.stmt_sequence(temp)
		# program = Node(node)
		self.out.write("program found\n")
		return root

	def stmt_sequence(self,node):
		node.add_child(self.statement())
		while self.top_token()[0] == ';':
			self.match(self.top_token()[0])
			node.add_child(self.statement())
		self.out.write("stmt-sequence found\n")
		return node

	def statement(self):
		if self.top_token()[0] == 'if':	temp = self.ifStmt()
		elif self.top_token()[0] == 'repeat':	temp = self.repeat_stmt()
		elif self.top_token()[1] == 'identifier': temp = self.assign_stmt()
		elif self.top_token()[0] == 'read': temp = self.read_stmt()
		elif self.top_token()[0] == 'write': temp = self.write_stmt() 
		else: self.error() 
		self.out.write("statement found\n")
		return temp

	def ifStmt(self):
		self.match('if')
		temp = t.Node("if"," ","r",True,False)
		temp.add_child(self.exp())
		self.match('then')
		temp_node = self.stmt_sequence(temp)
		simple = True
		if self.top_token()[0] == 'else':
			simple = False
			self.match('else')
			node = self.stmt_sequence(temp_node)
		self.match('end')
		self.out.write("if-stmt found\n")
		if simple:
			return temp_node
		return node

	def repeat_stmt(self):
		temp_node = t.Node("repeat"," ","r",True,False)
		self.match('repeat')
		node = self.stmt_sequence(temp_node)
		self.match('until')
		node.add_child(self.exp())
		self.out.write("repeat_stmt found\n")
		return node

	def assign_stmt(self):
		id = self.top_token()[0]
		self.match('identifier',True)
		self.match(':=')
		temp = t.Node("assign",id,"r",True,False)
		temp.add_child(self.exp())
		self.out.write("assign_stmt found\n")
		return temp

	def read_stmt(self):
		self.match('read')
		id = self.top_token()[0]
		self.match('identifier',True)
		self.out.write("read_stmt\n")
		return t.Node("read",id,"r",True,False)

	def write_stmt(self):
		self.match('write')
		temp = t.Node("write"," ","r",True,False)
		temp.add_child(self.exp())
		self.out.write("write_stmt found\n")
		return temp

	def exp(self):
		temp_node = self.simple_exp()
		simple = True
		if self.top_token()[0] == '<' or self.top_token()[0] == '=':
			simple = False
			temp = t.Node("comparison",self.top_token()[0],"e",True,True)
			self.match(self.top_token()[0])
			temp.add_child(temp_node)
			temp.add_child(self.simple_exp())
		self.out.write("exp found\n")
		if simple:
			return temp_node
		return temp


	def simple_exp(self):
		temp_node = self.term()
		simple = True
		while self.top_token()[0] == '+' or self.top_token()[0] == '-':
			simple = False
			temp = t.Node("op",self.top_token()[0],"e",True,True)
			temp.add_child(temp_node)
			self.match(self.top_token()[0])
			temp.add_child(self.term())
			temp_node = temp
		self.out.write("simple-exp found\n")
		if simple:
			return temp_node
		return temp



	def term(self):
		temp_node = self.factor()
		simple = True
		while self.top_token()[0] == "*":
			simple = False
			temp = t.Node("op","*","e",True,True)
			temp.add_child(temp_node)
			self.match(self.top_token()[0])
			temp.add_child(self.factor())
			temp_node = temp
		self.out.write("term found\n")
		if simple:
			return temp_node
		return temp

	def factor(self):
		" We'll assume that factor is number or identifier only just for now "
		if self.top_token()[0] == '(':
			self.match('(')
			temp = self.exp()
			self.match(')')
		elif self.top_token()[1] == 'number':
			temp = t.Node("number",self.top_token()[0],"e",True,True)
			self.match(self.top_token()[1],True)
		elif self.top_token()[1] == 'identifier':
			temp = t.Node("identifier",self.top_token()[0],"e",True,True)
			self.match(self.top_token()[1],True)
		else:	self.error()
		self.out.write("factor found\n")
		return temp

parser = Parser()
root = parser.program()
tree = t.Tree(root,500,500,scene)
levels = tree.get_levels(tree.root)
tree.print_tree(levels -1)
scene = tree.scene

view = QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing)
view.resize(1000, 600)
view.show()
app.exec_()