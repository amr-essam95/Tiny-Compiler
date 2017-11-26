import re

class Scanner(object):
	"""Scanner for the Tiny language"""
	output = ""
	tokens = []
	input_code = ""
	reserved_words = []

	def __init__(self):
		super(Scanner, self).__init__()
		self.output = open("scanner_output.txt","w")
		self.input_code = open("tiny_sample_code.txt")
		self.reserved_words = ["if","then","else","end","repeat","until","read","write"]
		# self.arg = arg

	""" Functions """
	def check_start(self,ch,i):
		if re.search("\d",ch):	return "in_num","start",ch,i+1
		elif re.search("[a-zA-Z]",ch): return "in_id","start",ch,i+1
		elif ch == ":": return "in_assign","start",ch,i+1
		elif ch == "{": return "in_comment","start",ch,i+1
		else: return "done","start",ch,i+1

	def check_in_num(self,ch,expr,i):
		if re.search("\d",ch):	return "in_num","start",expr + ch,i+1
		else: return "done","in_num",expr,i

	def check_in_id(self,ch,expr,i):
		if re.search("[a-zA-Z]",ch): return "in_id","start",expr + ch,i+1
		else: return "done","in_id",expr,i

	def check_in_assign(self,ch,expr,i):
		if ch == "=": return "done","in_assign",expr + ch,i+1
		else: return "done","start",expr,i
	def check_in_comment(self,expr,ch,i):
		if ch == "}": return "done","in_comment",expr + ch,i+1
		else: return "in_comment","start",expr + ch,i+1
	def print_expr(self,expr,last_state):
		if last_state == "in_id":
			if expr in self.reserved_words:
				self.output.write("%s : reserved word\n" % expr)
				self.tokens.append((expr,"reserved word"))
			else:								
				self.output.write("%s : identifier\n" % expr)
				self.tokens.append((expr,"identifier"))
		elif last_state == "in_num":			
			self.output.write("%s : number\n" % expr)
			self.tokens.append((expr,"number"))
		elif last_state == "in_assign":			
			self.output.write("%s : special symbol\n" % expr)
			self.tokens.append((expr,"special symbol"))
		elif last_state == "start":				
			self.output.write("%s : special symbol\n" % expr)
			self.tokens.append((expr,"special symbol"))
	def run(self):
		for line in self.input_code:
			line = line.rstrip()								#Remove the end of line characer
			i = 0
			while i < len(line):
				if line[i] ==  " ":								#Skip the spaces
					i += 1
					continue
				expr,state,last_state = "","start","start"		#Initialize the states
				while state != "done":
					if (state == "start"):			state,last_state,expr,i = self.check_start(line[i],i)
					elif (state == "in_num"):		state,last_state,expr,i = self.check_in_num(line[i],expr,i)
					elif (state == "in_id"): 		state,last_state,expr,i = self.check_in_id(line[i],expr,i)
					elif (state == "in_assign"): 	state,last_state,expr,i = self.check_in_assign(line[i],expr,i)
					elif (state == "in_comment"):	state,last_state,expr,i = self.check_in_comment(line[i],expr,i)
					if i == len(line) and state != "done":
					 	last_state = state
					 	state = "done"
				self.print_expr(expr,last_state)
		return self.tokens
	""" End of Functions """

scanner = Scanner()
scanner.run()