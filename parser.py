import re
from pptree import *
import scanner as sc
import tree as Tree


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
		node = self.stmt_sequence()
		program = Node(node)
		print "program found"
		print_tree(program)

	def stmt_sequence(self):
		self.statement()
		while self.top_token()[0] == ';':
			self.match(self.top_token()[0],x_root,y_root,scene,"r")
			self.statement()
		print "stmt-sequence found"

	def statement(self):
		if self.top_token()[0] == 'if':	self.ifStmt()
		elif self.top_token()[0] == 'repeat':	self.repeat_stmt()
		elif self.top_token()[1] == 'identifier': self.assign_stmt()
		elif self.top_token()[0] == 'read': self.read_stmt()
		elif self.top_token()[0] == 'write': self.write_stmt() 
		else: self.error() 
		print "statement found"

	def ifStmt(self):
		self.match('if')
		self.exp()
		temp = Tree("if"," ",)
		self.match('then')
		self.stmt_sequence()
		if self.top_token()[0] == 'else':
			self.match('else')
			self.stmt_sequence()
		self.match('end')
		print "if-stmt found"

	def repeat_stmt(self):
		self.match('repeat')
		self.stmt_sequence()
		self.match('until')
		temp = self.exp()
		print "repeat_stmt found"

	def assign_stmt(self):
		self.match('identifier',True)
		self.match(':=')
		temp = self.exp()
		print "assign_stmt found"

	def read_stmt(self):
		self.match('read')
		self.match('identifier',True)
		print "read_stmt"

	def write_stmt(self):
		self.match('write')
		temp = self.exp()
		print "write_stmt found"

	def exp(self):
		temp = self.simple_exp()
		if self.top_token()[0] == '<' or self.top_token()[0] == '=':
			tree = Tree("comparison",self.top_token()[0],x_root,y_root,scene,"e")
			self.match(self.top_token()[0])
			self.simple_exp()
		print "exp found"


	def simple_exp(self):
		temp = self.term()
		while self.top_token()[0] == '+' or self.top_token()[0] == '-':
			tree = Tree("addop",self.top_token()[0],x_root ,y_root,scene,"e")
			tree.append(temp)
			self.match(self.top_token()[0])
			temp2 = self.term()
			tree.append(temp2)
			temp = tree
		print "simple-exp found"
		return temp



	def term(self):
		temp = self.factor()
		while self.top_token()[0] == "*":
			tree = Tree("mulop","*",x_root,y_root,scene,"e")
			tree.append(temp)
			self.match(self.top_token()[0])
			temp2 = self.factor()
			tree.append(temp2)
			temp = tree
		print "term found"
		return temp

	def factor(self):
		if self.top_token()[0] == '(':
			self.match('(')
			temp = self.exp()
			self.match(')')
		elif self.top_token()[1] == 'number':
			temp = Tree("number",self.top_token()[1],x_root,y_root,scene,"e")
			self.match(self.top_token()[1],True)
		elif self.top_token()[1] == 'identifier':
			self.match(self.top_token()[1],True)
			temp = Tree("identifier",self.top_token()[1],x_root,y_root,scene,"e")
		else:	self.error()
		print "factor found"
		return temp

parser = Parser()
parser.program()