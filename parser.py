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
		print "program found"
		return root

	def stmt_sequence(self,node):
		node.add_child(self.statement())
		while self.top_token()[0] == ';':
			self.match(self.top_token()[0])
			node.add_child(self.statement())
		print "stmt-sequence found"
		return node

	def statement(self):
		if self.top_token()[0] == 'if':	temp = self.ifStmt()
		elif self.top_token()[0] == 'repeat':	temp = self.repeat_stmt()
		elif self.top_token()[1] == 'identifier': temp = self.assign_stmt()
		elif self.top_token()[0] == 'read': temp = self.read_stmt()
		elif self.top_token()[0] == 'write': temp = self.write_stmt() 
		else: self.error() 
		print "statement found"
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
		print "if-stmt found"
		if simple:
			return temp_node
		return node

	def repeat_stmt(self):
		temp_node = t.Node("repeat"," ","r",True,False)
		self.match('repeat')
		node = self.stmt_sequence(temp_node)
		self.match('until')
		node.add_child(self.exp())
		print "repeat_stmt found"
		return node

	def assign_stmt(self):
		id = self.top_token()[0]
		self.match('identifier',True)
		self.match(':=')
		temp = t.Node("assign",id,"r",True,False)
		temp.add_child(self.exp())
		print "assign_stmt found"
		return temp

	def read_stmt(self):
		self.match('read')
		id = self.top_token()[0]
		self.match('identifier',True)
		print "read_stmt"
		return t.Node("read",id,"r",True,False)

	def write_stmt(self):
		self.match('write')
		temp = t.Node("write"," ","r",True,False)
		temp.add_child(self.exp())
		print "write_stmt found"
		return temp

	def exp(self):
		temp_node = self.simple_exp()
		simple = True
		if self.top_token()[0] == '<' or self.top_token()[0] == '=':
			simple = False
			temp = t.Node("comparison",self.top_token()[0],"e",True,True)
			temp.add_child(temp_node)
			self.match(self.top_token()[0])
			temp.add_child(self.simple_exp())
		print "exp found"
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
		print "simple-exp found"
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
		print "term found"
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
			temp = t.Node("number",self.top_token()[1],"e",True,True)
			self.match(self.top_token()[1],True)
		elif self.top_token()[1] == 'identifier':
			self.match(self.top_token()[1],True)
			temp = t.Node("identifier",self.top_token()[1],"e",True,True)
		else:	self.error()
		print "factor found"
		return temp

parser = Parser()
root = parser.program()
tree = t.Tree(root,500,500,scene)
tree.print_tree(6)
scene = tree.scene

view = QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing)
view.resize(1000, 600)
view.show()
app.exec_()