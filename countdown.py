#!/bin/env python3

import operator
from itertools import permutations, combinations_with_replacement, product
from more_itertools import distinct_permutations
DEFAULT_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


#check if a sequence is a valid postfix notation
def is_valid(sequence):
    count_nums = 0
    for token in sequence:
        if not token:
            count_nums -= 1
            if count_nums < 1:
                return False
        else:
            count_nums +=1
    return True

#generate all valid postfix sequences
def valid_sequences(num_count):
    base = (True,) * num_count + (False,) * (num_count - 1)
    perms = distinct_permutations(base) 

    for sequence in perms:
        if is_valid(sequence):
            yield sequence


#generate all possible permutations
def distinct_ordered_combinations(iterable, r):
    seen = set()
    for combination in combinations_with_replacement(iterable, r):
        for permutation in permutations(combination):
            if permutation not in seen:
                yield permutation
                seen.add(permutation)

def generate_sequences(numbers, operators):
    l = len(numbers)
    for sequence in valid_sequences(l):
        for nums, ops in product(
                distinct_permutations(numbers),
                distinct_ordered_combinations(operators, l - 1),
        ):
            nums = iter(nums)
            ops = iter(ops)
            yield tuple(next(nums) if token else next(ops) for token in sequence)

#calculate the result of a sequence
class FalseOperation(ValueError):
    pass
    
def calculate_sequence(sequence, operators):
    stack = list(sequence[:2])
    for idx, token in enumerate(sequence[2:], start=3):
        if token not in operators:
            stack.append(token)
            continue
        operand2 = stack.pop()
        operand1 = stack.pop()
        try:
            result = operators[token](operand1, operand2)
        except ZeroDivisionError:
            raise FalseOperation('Division by zero')
        if int(result) != result:
            raise FalseOperation('non-int value')
        if result < 0:
            raise FalseOperation('negative value')
        yield result, sequence[:idx]
        stack.append(result)

def solve(target, numbers, operators = DEFAULT_OPERATORS):
	for sequence in generate_sequences(numbers, operators):
		try:
			for result , seq in calculate_sequence(sequence, operators):
				if result == target:
					return seq
		except FalseOperation:
			pass
	return None


def isOperand(x): 
    return ((x >= 'a' and x <= 'z') or 
            (x >= 'A' and x <= 'Z'))  

def getInfix(exp): 
    stack = []
    for i, e in enumerate(exp):
    	if str(e) not in "+-/*":
    		stack.append(str(e))
    	else:
    		operator1 = stack.pop()
    		operator2 = stack.pop()

    		stack.append("(" + operator2 + str(e) + operator1 + ")")
    return stack.pop()


def matchWord(word1, word2):
    isMatch = True
    for letter in word1:
        if letter in word2:
            word2.remove(letter)
        else:
            isMatch = False
    if len(word2) == 0:
            isMatch = True
    return isMatch


def solve_number(n, t):
	opl = solve(t, n)
	print(getInfix(opl))
	print(eval(getInfix(opl)))

def solve_word(letters):
	longestWord = ""
	matches = []
	with open("wordlist.txt", "r") as infile:
		for word in infile:
			word = word.strip()
			if matchWord(list(letters), list(word)):
				matches.append(word)
		return matches 

if __name__ == '__main__':


	tmp = input("what round is it?")
	while tmp not in ["letters", "numbers"]:
		print("not a valid round, try again!")
		tmp = input("what round is it?")

	if tmp == "letters":
		letters = [input("give me the letter: ") for i in range(int(input("How many letters?")))]
		for solution in sorted(solve_word(letters),key=len):
			print(solution)

	else:
		numbers = [int(input("give me the number: ")) for i in range(int(input("How many numbers?")))]
		target = int(input("what is the target? "))

		solve_number(numbers, target)

	