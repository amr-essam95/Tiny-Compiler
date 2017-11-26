import re
import scanner as sc
class Parser(object):
	"""Parser for the Tiny Language"""
	tokens = ""

	def __init__(self):
		super(Parser, self).__init__()
		scanner = sc.Scanner()
		self.tokens = scanner.run()
		# print self.tokens
		# self.arg = arg
		
	def get_token():
		""" This function get the in order token and proceed to the next token"""
		pass

	def top_token():
		""" This function gets the in order token but don't proceed to the next token"""
		pass

	def error():
		pass


	def match(expected_token):
		token = top_token()
		if token == expected_token:		get_token()
		else:		error()

	def ifStmt():
		token = top_token()
		match('if')
		match('(')
		exp()
		match(')')
		statement()
		if token == 'else':
			match('else')
			statement()


	def exp():
		token = top_token()
		term()
		while token == '+' or token == '-':
			match(token)
			term()
			token = top_token()

	def statement():
		pass

	def term():
		token = top_token()
		factor()
		while token == "*":
			match(token)
			factor()
			token = top_token()

	def factor():
		token = top_token()
		if token == '(':
			match('(')
			exp()
			match(')')
		elif token.isdigit():
			match(token)
		else:	error()

parser = Parser()