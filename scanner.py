import re

output = open("scanner_output.txt","w")
input_code = open("tiny_sample_code.txt")
reserved_words = ["if","then","else","end","repeat","until","read","write"]

""" Functions """
def check_start(ch,i):
	if re.search("\d",ch):	return "in_num","start",ch,i+1
	elif re.search("[a-zA-Z]",ch): return "in_id","start",ch,i+1
	elif ch == ":": return "in_assign","start",ch,i+1
	elif ch == "{": return "in_comment","start",ch,i+1
	else: return "done","start",ch,i+1

def check_in_num(ch,expr,i):
	if re.search("\d",ch):	return "in_num","start",expr + ch,i+1
	else: return "done","in_num",expr,i

def check_in_id(ch,expr,i):
	if re.search("[a-zA-Z]",ch): return "in_id","start",expr + ch,i+1
	else: return "done","in_id",expr,i

def check_in_assign(ch,expr,i):
	if ch == "=": return "done","in_assign",expr + ch,i+1
	else: return "done","start",expr,i
def check_in_comment(ch,i):
	if ch == "}": return "done","in_comment",expr + ch,i+1
	else: return "in_comment","start",expr + ch,i+1
def print_expr(expr,last_state):
	if last_state == "in_id":
		if expr in reserved_words:	output.write("%s : reserved word\n" % expr)
		else:	output.write("%s : identifier\n" % expr)
	elif last_state == "in_num":	output.write("%s : number\n" % expr)
	elif last_state == "in_assign":	output.write("%s : special symbol\n" % expr)
	elif last_state == "start":		output.write("%s : special symbol\n" % expr)
""" End of Functions """

for line in input_code:
	line = line.rstrip()								#Remove the end of line characer
	i = 0
	while i < len(line):
		if line[i] ==  " ":								#Skip the spaces
			i += 1
			continue
		expr,state,last_state = "","start","start"		#Initialize the states
		while state != "done":
			if (state == "start"):			state,last_state,expr,i = check_start(line[i],i)
			elif (state == "in_num"):		state,last_state,expr,i = check_in_num(line[i],expr,i)
			elif (state == "in_id"): 		state,last_state,expr,i = check_in_id(line[i],expr,i)
			elif (state == "in_assign"): 	state,last_state,expr,i = check_in_assign(line[i],expr,i)
			elif (state == "in_comment"):	state,last_state,expr,i = check_in_comment(line[i],i)
			if i == len(line) and state != "done":
			 	last_state = state
			 	state = "done"
		print_expr(expr,last_state)