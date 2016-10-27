import sys, copy, re

def splitStatement(statement):
	clauses = statement.split("&&")
	rules = []
	for clause in clauses:
		clause = clause.replace(")","")
		clause = clause.split("(")
		clause[1] = clause[1].split(",")
		rules = rules + clause
	return rules

def createRules(statements, noOfStatements):
	num = 0
	for i in range(0,noOfStatements):
		statements[i] = statements[i].replace(" ", "")
		varMap = {}
		if "=>" in statements[i]:
			brokenStatement = statements[i].split("=>")
			left = splitStatement(brokenStatement[0])
			for j in range(len(left)/2):
				for k in range(len(left[2 * j + 1])):
					if left[2 * j + 1][k][0].islower():
						if left[2 * j + 1][k] not in varMap.keys():
							varMap[left[2 * j + 1][k]] = 'a'+`num`
							num = num + 1
						left[2 * j + 1][k] = varMap[left[2 * j + 1][k]]
			lhs.append(left)
			right = splitStatement(brokenStatement[1])
			for j in range(len(right)/2):
				for k in range(len(right[2 * j + 1])):
					if right[2 * j + 1][k][0].islower():
						if right[2 * j + 1][k] not in varMap.keys():
							varMap[right[2 * j + 1][k]] = 'a'+`num`
							num = num + 1
						right[2 * j + 1][k] = varMap[right[2 * j + 1][k]]
			rhs.append(right)
		else:
			lhs.append([])
			right = splitStatement(statements[i])
			for j in range(len(right)/2):
				for k in range(len(right[2 * j + 1])):
					if right[2 * j + 1][k][0].islower():
						if right[2 * j + 1][k] not in varMap.keys():
							varMap[right[2 * j + 1][k]] = 'a'+`num`
							num = num + 1
						right[2 * j + 1][k] = varMap[right[2 * j + 1][k]]
			rhs.append(right)

def unify(unified, ununified, toUnify):
	workingCopy = copy.deepcopy(toUnify)
	unifiedLiterals = unified[1::2]
	ununifiedLiterals = ununified[1::2]
#	print unified
#	print ununified
#	print 'To Unify: ', workingCopy
#	print unifiedLiterals
#	print ununifiedLiterals
	for i in range(len(unifiedLiterals)):
		for j in range(len(unifiedLiterals[i])):
			if unifiedLiterals[i][j] != ununifiedLiterals[i][j] and ununifiedLiterals[i][j][0].islower():
#				print unifiedLiterals[i][j], ununifiedLiterals[i][j]
				#and unifiedLiterals[i][j][0].isupper():
				for k in range(len(workingCopy[1::2])):
					workingCopy[2 * k + 1] = [unifiedLiterals[i][j] if x == ununifiedLiterals[i][j] else x for x in workingCopy[2 * k + 1]]
#	print 'Unified: ', workingCopy
	return workingCopy

def printStatement(fn, statement):
	fn = fn + ':'
	literals = copy.deepcopy(statement[1])
	workingCopy = copy.deepcopy(statement)
	for l in range(len(literals)):
		if literals[l][0].islower():
			literals[l] = '_'
	literalsString = ", ".join(literals)
	workingCopy[1] = literalsString
	completeString = "(".join(workingCopy)
	completeString = completeString + ')'
	traverseLog.write(fn + completeString + '\n')

def ask(statement, parent, noOfChildren):
	query = copy.deepcopy(statement[0:2])
	remainder = copy.deepcopy(statement[2:len(statement)])
	if all(term[0].isupper() for term in query[1]):
		if query in rhs:
			print '0 Ask: ', query
			#printStatement('Ask', query)
			print '1 True: ', query
			#printStatement('True', query)
			print '99', query, parent, noOfChildren - 1
			if len(parent) > 0 and noOfChildren - 1 == 0:
				print '1.1 True: ', parent
				#printStatement('True', parent)
			if len(remainder) > 0:
				print '100', remainder, parent, (noOfChildren - 1 if noOfChildren > 0 else 0)
				result = ask(remainder, parent, (noOfChildren - 1 if noOfChildren > 0 else 0))
				if result is not True and result is not False:
					return query + result
				else:
					return result
			else:
				return True
		else:
			for i in range(len(rhs)):
				if query[0] == rhs[i][0] and any(j[0].islower() for j in rhs[i][1]):
					print '2 Ask: ', query
					#printStatement('Ask', query)
					unified = unify(query, rhs[i], lhs[i])
					print '101', unified, query, len(unified)/2
					tryResult = ask(unified, query, len(unified)/2)
					print parent, tryResult
					if tryResult is not False:
						if tryResult is not True:
							print '3 True: ', query
							#printStatement('True', query)
							if len(parent) > 0 and noOfChildren - 1 == 0:
								print '3.1 True: ', parent
								#printStatement('True', parent)
						if len(remainder) > 0:
							print '102', remainder, parent, (noOfChildren - 1 if noOfChildren > 0 else 0)
							result = ask(remainder, parent, (noOfChildren - 1 if noOfChildren > 0 else 0))
							if result is True:
								return True
							elif result is not False:
								return query + result
							else:
								return False
						else:
							return True
			print '4 Ask: ', query
			#printStatement('Ask', query)
			print '5 False: ', query
			#printStatement('False', query)
			return False
	else:
		for i in range(len(rhs)):
			if query[0] == rhs[i][0] and all(query[1][j] == rhs [i][1][j] for j in range(len(query[1])) if rhs[i][1][j][0].isupper() and query[1][j][0].isupper()):
				if all(term[0].isupper() for term in rhs[i][1]):
					print '6 Ask: ', query
					#printStatement('Ask', query)
					print '7 True: ', rhs[i]
					#printStatement('True', rhs[i])
					#noOfChildren = noOfChildren - 1
					if len(parent) > 0 and noOfChildren - 1 == 0:
						print '8 True: ', parent
						#printStatement('True', parent)
					if len(remainder) > 0:
						attempt = unify(rhs[i], query, remainder)
						print '103', attempt, parent, (noOfChildren - 1 if noOfChildren > 0 else 0)
						result = ask(attempt, parent, (noOfChildren - 1 if noOfChildren > 0 else 0))
						if  result is not False:
							return rhs[i] + attempt
					else:
						return rhs[i]
				else:
					#t = unify(rhs[i],query,query)
					print '8.1 Ask: ', query
					#print '8.2 Ask: ', t
					#printStatement('Ask', query)
					unified = unify(query, rhs[i], lhs[i])
					#unified = unify(t, query, unified)
					unified = unified + query + remainder
					print '104', unified, query, len(lhs[i])/2
					tryResult = ask(unified, query, len(lhs[i])/2)
					if tryResult is not False:
						#print '8 True: ', query
						#printStatement('True', tryResult)
						return tryResult
		print '9 False: ', query
		#printStatement('False', query)
		return False

if __name__ == '__main__':
	filename = sys.argv[-1]
	file = open(filename, 'r')

	task = file.readline().rstrip()
	task = task.replace(" ", "")
	task = splitStatement(task)

	noOfStatements = int(file.readline().rstrip())
	statements = [next(file).rstrip() for x in xrange(noOfStatements)]

	global lhs
	lhs = []
	global rhs
	rhs = []
	global used
	used = []
	global traverseLog
	traverseLog = open('output.txt','w')

	createRules(statements,noOfStatements)

#	print unify(['Traitor', ['Anakin']],['Traitor', ['x']],['ViterbiSquirrel', ['x'], 'Secret', ['y'], 'Tells', ['x', 'y', 'z'], 'Hostile', ['z']])
#	print unify(['Faster', ['Bob', 'Steve']],['Faster', ['x', 'y']],['Buffalo', ['x'], 'Pig', ['y']])
#	print unify(['Parent', ['Kevin', 'Jane']],['Parent', ['p', 'Jane']],['Parent', ['p', 'Jane'], 'Parent', ['p', 'b']])
#	print task
#	print lhs
#	print rhs
	if ask(task, [], 0) is not False:
		traverseLog.write("True")
	else:
		traverseLog.write("False")
