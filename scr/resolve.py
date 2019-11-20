import sys
import re

class equation_operand:
	
	def __init__(self):
		self.sign = None
		self.number = None
		self.x = False
		self.power = None
		self.to_reduce = False
		self.name = None

	def set_sign(self, sign):
		self.sign = sign

	def set_number(self, number):
		self.number = number

	def set_x(self, x):
		self.x = x

	def set_power(self, power):
		self.power = power

	def set_to_reduce(self, to_reduce):
		self.to_reduce = to_reduce

	def set_operand_name(self, name):
		self.name = name

	def get_number(self):
		return (float(self.number) * float(self.sign))

	def set_all_value(self, sign, number, x, power, to_reduce, name):
		self.sign = sign
		self.number = number
		self.x = x
		self.power = power
		self.to_reduce = to_reduce
		self.name = name

def parsing(equation_string):

	equation = []
	equal_passed = 0
	equation_string = equation_string.replace(' ', '')
	#syntax check if power > 0
	if equation_string.find("^-2") != -1:
		print("Unexpected syntax: '^-2'")
		exit(1)
	if equation_string.find("^-1") != -1:
		print("Unexpected syntax: '^-1'")
		exit(1)
	if equation_string.find("^-0") != -1:
		print("Unexpected syntax: '^-0'")
		exit(1)

	equation_string_split = re.split("(\+|\-|\=)", equation_string)

	for i in range(len(equation_string_split)):
		if equation_string_split[i] == '=':
			equal_passed = 1
		if equation_string_split[i] != '+' and equation_string_split[i] != '-' and equation_string_split[i] != '=':
			#create object equation_operand
			equation_part = equation_operand()

			#set to_reduce of the equation_operand_obj
			if equal_passed == 1:
				equation_part.set_to_reduce(True)

			#set sign of the equation_operand_obj
			if i > 0 and equation_string_split[i - 1] != '=':
				if equation_string_split[i - 1] == '-':
					equation_part.set_sign(-1)
				elif equation_string_split[i - 1] == '+':
					equation_part.set_sign(1)
			else:
				equation_part.set_sign(1)

			#set x of the equation_operand_obj
			if equation_string_split[i].find('X') != -1:
				equation_part.set_x(True)

			#set number of the equation_operand_obj
			multiplicator_index = equation_string_split[i].find('*')
			if multiplicator_index != -1:
				equation_part.set_number(equation_string_split[i][0:multiplicator_index])
			else:
				if equation_string_split[i].find('X') != -1: #if there is only "X ^ number" then is equal to 1
					equation_part.set_number(1)
				else:
					equation_part.set_number(equation_string_split[i])


			#set power of the equation_operand_obj
			power_index = equation_string_split[i].find('^')
			if power_index != -1: #we check if there a power in the string in case there in only "number * X"
				equation_part.set_power(equation_string_split[i][power_index + 1])
			elif power_index == -1 and multiplicator_index != -1: #if there no power in the string only a X
				equation_part.set_power(1)
			else: #if there is only a number
				equation_part.set_power(0)


			#set name of operand like : a,b,c
			equation_part.set_operand_name(chr(99 - int(equation_part.power))) #get ascii number c = 99 and subtract power to it so a = 99 - 2 and b = 99 - 1


			#add the equation_operand object to an equation_tab who contain all part of the equation
			equation.append(equation_part)

	return equation



def reduce(equation):
	for i in range(len(equation)):
		find_correspondance_name = 0
		if equation[i].to_reduce == True: #if we find a part to reduce
			for j in range(len(equation)):
				if equation[i].name == equation[j].name and equation[j].to_reduce != True: #if we find the equivalent like part "a to reduce" we search 'a' 
					find_correspondance_name = 1
					if equation[i].sign == 1:
						equation[j].number = float(equation[j].number) - float(equation[i].number)
					else:
						equation[j].number = float(equation[j].number) + float(equation[i].number)

			#if there is no correspondance with the operand to reduce in name, we just pass the operand to no_reduce and multiplicate is number by -1
			if find_correspondance_name == 0 and float(equation[i].number) != 0.0:
				equation[i].to_reduce = False
				equation[i].number = (equation[i].get_number() * -1)

	for i in range(len(equation)):  # we add all the same part together, like a + a / b + b...
		for j in range(len(equation)):
			if equation[i].name == equation[j].name and i != j and (equation[j].to_reduce != True and equation[i].to_reduce != True):
				if equation[j].sign == 1:
					equation[i].number = float(equation[i].number) + float(equation[j].number)
				else:
					equation[i].number = float(equation[i].number) - float(equation[j].number)
				equation[j].to_reduce = True

	equation = [x for x in equation if not float(x.number) == 0.0] #remove all the equation_part with a number equal to 0
	equation = [x for x in equation if not x.to_reduce == True] #remove all the equation_part who where after the equal because they was reduce

	return equation

def get_degree(equation):
	degree = 0
	for i in range(len(equation)):
		if int(equation[i].power) > degree:
			degree = int(equation[i].power)
	return degree

def resolve(equation, degree):
	if degree > 2:
		print("The polynomial degree is stricly greater than 2, I can't solve.")
		
	if degree == 2:
		a_item = [x for x in equation if x.name == 'a'] # we get the a part of the equation
		b_item = [x for x in equation if x.name == 'b']	# we get the b part of the equation
		c_item = [x for x in equation if x.name == 'c']	# we get the c part of the equation

		if not b_item:
			b_item = [equation_operand()]
			b_item[0].set_all_value(1, 0.0, True, 1, False, 'b')
		if not c_item:
			c_item = [equation_operand()]
			c_item[0].set_all_value(1, 0.0, True, 0, False, 'c')

		a = a_item[0].get_number()
		b = b_item[0].get_number()
		c = c_item[0].get_number()
		discriminant = (b ** 2) - (4 * a * c)
		print("a = " + str(a) + "\nb = " + str(b) + "\nc = " + str(c) + "\ndiscriminant = " + str(discriminant))
		if discriminant > 0:
			solution_1 = ((-b - (discriminant ** 0.5)) / (2.0 * a))
			solution_2 = ((-b + (discriminant ** 0.5)) / (2.0 * a))
			print("Discriminant is strictly positive, the two solutions are:\nsolution 1: " + str(solution_1) + "\nsolution 2: " + str(solution_2))
		elif discriminant == 0:
			solution = (-b / (2 * a))
			print("Discriminant is equal to 0, the solution is:\nsolution : " + str(solution))
		else:
			solution_1 = ((-b - ((discriminant * -1) ** 0.5)) / (2.0 * a))
			solution_2 = ((-b + ((discriminant * -1) ** 0.5)) / (2.0 * a))
			print("Discriminant is strictly negative, the two solutions are:\nsolution 1: " + str(solution_1) + "i" +"\nsolution 2: " + str(solution_2)) + "i"

	elif degree == 1:
		a_item = [x for x in equation if x.name == 'b'] # we get the a part of the equation
		b_item = [x for x in equation if x.name == 'c']	# we get the b part of the equation

		if not b_item:
			b_item = [equation_operand()]
			b_item[0].set_all_value(1, 0.0, True, 0, False, 'b')

		a = a_item[0].get_number()
		b = b_item[0].get_number()
		print("a = " + str(a) + "\nb = " + str(b))
		if a != 0.0 and b != 0.0:
			solution = (-b / a)
			print("solution : " + str(solution))
		elif b == 0.0 and a != 0.0:
			print("b is equal to zero the solution is 0.0")
		elif b != 0.0 and a == 0.0:
			print("there is no solution")

	elif degree == 0:
		a_item = [x for x in equation if x.name == 'c']

		if not a_item:
			a_item = [equation_operand()]
			a_item[0].set_all_value(1, 0.0, True, 0, False, 'b')

		a = a_item[0].get_number()
		if (a != 0):
			print("there is no solution")
		else:
			print("every real are solution")

def print_equation(equation):
	str_equation = "Reduced form: "
	for i in range(len(equation)):
		if i > 0:
			if equation[i].sign == 1:
				str_equation += '+ '
			else:
				str_equation += '- '
		str_equation += str(float(equation[i].number)) + " " 
		if int(equation[i].power) > 0:
			if int(equation[i].power) == 1:
				str_equation += "* X "
			elif int(equation[i].power) >= 2:
				str_equation += "* X ^ " + equation[i].power + " "
	str_equation += "= 0.0"
	print(str_equation)

	
if len(sys.argv) < 2 or len(sys.argv) > 2:
	print("no arguments or too much arguments")
	exit(1)
equation = parsing(sys.argv[1])
equation = reduce(equation)
degree = get_degree(equation)
print_equation(equation)
print("Polynomial degree: " + str(degree))
resolve(equation, degree)
