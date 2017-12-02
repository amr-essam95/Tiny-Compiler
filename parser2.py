import re
from pptree import *
import scanner as sc
# import tree as Tree


# scene = QGraphicsScene()
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
		# print_tree(program)

	def stmt_sequence(self):
		self.statement()
		while self.top_token()[0] == ';':
			self.match(self.top_token()[0])
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
		# temp = Tree("if"," ",x_root,y_root,scene,"e")
		# temp.append
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
		self.exp()
		print "repeat_stmt found"

	def assign_stmt(self):
		self.match('identifier',True)
		self.match(':=')
		self.exp()
		print "assign_stmt found"

	def read_stmt(self):
		self.match('read')
		self.match('identifier',True)
		print "read_stmt found"

	def write_stmt(self):
		self.match('write')
		self.exp()
		print "write_stmt found"

	def exp(self):
		self.simple_exp()
		if self.top_token()[0] == '<' or self.top_token()[0] == '=':
			self.match(self.top_token()[0])
			self.simple_exp()
		print "exp found"


	def simple_exp(self):
		self.term()
		while self.top_token()[0] == '+' or self.top_token()[0] == '-':
			self.match(self.top_token()[0])
			self.term()
		print "simple-exp found"



	def term(self):
		self.factor()
		while self.top_token()[0] == "*":
			self.match(self.top_token()[0])
			self.factor()
		print "term found"

	def factor(self):
		if self.top_token()[0] == '(':
			self.match('(')
			self.exp()
			self.match(')')
		elif self.top_token()[1] == 'number':
			self.match(self.top_token()[1],True)
		elif self.top_token()[1] == 'identifier':
			self.match(self.top_token()[1],True)
		else:	self.error()
		print "factor found"

parser = Parser()
parser.program()