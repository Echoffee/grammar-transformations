import copy
class node:
	def __init__(self, parent) :
		self.P = parent
		self.O = [] 	#objet : [type (string), name (string), arity (int), args (string[])]
		self.C = []		#childs
		self.B = False  #marker t/f : to identify sub-trees (findPattern, etc...)
		if parent != None:
			parent.addChild(self)

	def setObject(self, o):
		self.O = o
		
	def getObject(self):
		return self.O
		
	def setParent(self, p):
		self.P = p
		
	def getParent(self):
		return self.P
		
	def addChild(self, c):
		self.C = self.C + [c]
		
	def insertChild(self, index, c):
		if len(self.C) <= index:
			self.addChild(c)
		else:
			self.C.insert(index, c)
		
	def setChilds(self, childs):
		self.C = childs
		
	def getChilds(self):
		return self.C
		
	def removeChild(self, child):
		for c in self.C :
			if child.getObject()[1] == c.getObject()[1]:
				i = self.C.index(c)
				self.C.remove(c)
				return i
	
	def mark(self, b):
		self.B = b
		
	def isMarked(self):
		return self.B
	
	### old ###
	def paths(self, s, P, final, branch):
		#gives a list of all possible paths (only labels)
		if (branch > 0):
			s = s + [branch] + [self.O[1]]
		else :
			s = s + [self.O[1]]
		if len(self.C) == 0:
			P = P + [s]
			final.append(P)
		else:
			for b in range(len(self.C)):
				self.C[b].paths(s, P, final, b + 1)


def getLeafs(tree):
	# Returns a list of the given tree's leafs (node without childs)
	result = []
	r_getLeafs(tree, result)
	return result
	
def r_getLeafs(tree, result):
	# Recursive call for getLeafs()
	if len(tree.getChilds()) == 0:
		result = result + [tree]
	else:
		for n in tree.getChilds():
			r_getLeafs(n, result)
			
def findPattern(tree, pattern):
	# Find the first subtree (top-left) in a given tree, returns first node position if found or null if not
	# Top node of the subtree will be returned, and all the marked nodes connected to it are a part of the subtree
	# result = [bool, node]
	result = r_findPattern(tree, pattern, [False, None])
	return result[1]
	
# def findPatterns(tree, pattern):
# 	# Find all of the subtrees in a given tree
# 	# Top node of each subtree will be returned, and all the connected marked nodes to it are a part of the subtree
# 	rl = []
# 	patternLeafs = getLeafs(pattern)
# 	treeLeafs = getLeafs(tree)
# 	sn = []
# 	for tl in treeLeafs:
# 		r = []
# 		r_findPatterns(tl, patternLeafs, sn, r)
# 
# 	return rl
# 
# def r_findPatterns(treeLeaf, patternLeafs, pastNodes, result):
# 	if treeLeaf not in pastNodes:
# 		pastNodes = pastNodes + []
# 		l = list(filter(lambda x : x.getObject()[1] == treeLeaf.getObject()[1], patternLeafs))
# 		if len(l) > 0:
# 			

def r_findPattern(tree, pattern, result):
	# Recursive call for findPattern()
	if tree.getObject()[1] == pattern.getObject()[1] and not tree.isMarked():
		if len(pattern.getChilds()) == 0 and len(tree.getChilds()) == 0:
			tree.mark(True)
			return [True, tree]
		else :
			b = [True, tree]
			if (len(pattern.getChilds()) > 0) and len(pattern.getChilds()) == len(tree.getChilds()):
				for i in range(len(tree.getChilds())):
					nb = r_findPattern(tree.getChilds()[i], pattern.getChilds()[i], [True, tree])
					b = [b[0] and nb[0], tree]
				
			if b[0] :
				tree.mark(True)
				return b
			else :
				b = [False, None]
				for i in range(len(tree.getChilds())):
					v = r_findPattern(tree.getChilds()[i], pattern, [False, None])
					b = [b[0] and v[0], (b[1] if v[1] == None else v[1])]
					
				return b
	else :
		if result[0] :
			return [False, None]
		else:
			b = [False, None]
			for i in range(len(tree.getChilds())):
				v = r_findPattern(tree.getChilds()[i], pattern, [False, None])
				b = [b[0] or v[0], (b[1] if v[1] == None else v[1])]
				
			return b

def findPatternWithParams(tree, pattern):
	# Find the first subtree (top-left) in a given tree using parameters (v1, v2, ...), returns first node position if found or null if not
	# Top node of the subtree will be returned, and all the marked nodes connected to it are a part of the subtree, parameters exclued
	# result = [bool, node, [param1, param2, ...]]
	params = []
	for p in pattern.getObject()[3]:
		params = params + [[p, None]]
		
	result = r_findPatternWithParams(tree, pattern.getChilds()[0], [False, None], params, pattern.getChilds()[0])
	return [result[1], params]
	

def r_findPatternWithParams(tree, pattern, result, params, origin):
	# Recursive call for findPatternWithParams()
	if pattern.getObject()[0] == "P":
		p = next(filter(lambda x : x[0] == pattern.getObject()[1], params))
		if p[1] == None:
			p[1] = tree
			return [True, tree]
		else:
				return [r_compareTree(tree, p[1]), tree]
				
	elif tree.getObject()[1] == pattern.getObject()[1]:
		if len(pattern.getChilds()) == 0 and len(tree.getChilds()) == 0:
			tree.mark(True)
			return [True, tree]
		else :
			b = [True, tree]
			if (len(pattern.getChilds()) > 0) and len(pattern.getChilds()) == len(tree.getChilds()):
				for i in range(len(tree.getChilds())):
					nb = r_findPatternWithParams(tree.getChilds()[i], pattern.getChilds()[i], [True, tree], params, origin)
					b = [b[0] and nb[0], tree]
				
			if b[0] :
				tree.mark(True)
				return b
			else :
				b = [False, None]
				for i in range(len(tree.getChilds())):
					v = r_findPatternWithParams(tree.getChilds()[i], pattern, [False, None], params, origin)
					b = [b[0] and v[0], (b[1] if v[1] == None else v[1])]
					
				return b
	else :
		if result[0] :
			if origin != pattern:
				for ppp in params:
					ppp[1] = None
					
				return [False, None]
			else:
				return [False, None]
		else:
			b = [False, None]
			for i in range(len(tree.getChilds())):
				v = r_findPatternWithParams(tree.getChilds()[i], pattern, [False, None], params, origin)
				b = [b[0] or v[0], (b[1] if v[1] == None else v[1])]
				
			return b

def r_compareTree(t1, t2):
	# Compares 2 trees, returns True if t1 = t2 (labels)
	if t1.getObject()[1] == t2.getObject()[1]:
		if len(t1.getChilds()) == 0 and len(t2.getChilds()) == 0:
			return True
		elif len(t1.getChilds()) == len(t2.getChilds()) :
			b = True
			for i in range(len(t1.getChilds())):
				b = b and r_compareTree(t1.getChilds()[i], t2.getChilds()[i])
			
			return b
		else:
			return False
	else:
		return False

def replaceInTree(startingNode, newPatterns, args = []):
	if (args == []):
		args = startingNode.getObject()[3]
	
	r_replaceInTree(args, startingNode, newPatterns)

# Wrong behavior : change f(v1, v2) to f(t', t'')
def r_replaceInTree(args, currentNode, newPatterns, index = 0):
	if currentNode.getObject()[0] == "P":		# value type : P = parameter (v1, v2, ...); T = terminal (a, b, f, ...); NT = non-terminal (phi, psi, ...)
		i = args.index(currentNode.getObject()[1])
		if (i < len(newPatterns)):
			n = copy.deepcopy(newPatterns[i])
			n.setParent(currentNode.getParent())
			currentNode.getParent().insertChild(index, n)
	else :
		for x in range(len(currentNode.getChilds())):
			r_replaceInTree(args, currentNode.getChilds()[x], newPatterns, index = x)



def replaceInTree2(oldNode, newNode):
	# Replace an old node (o) by a new one (n)
	# E.g. f(o(a, b)) => f(n(a')) (with a != a')
	p = oldNode.getParent()
	i = p.removeChild(oldNode)
	if i != None:
		p.insertChild(i, newNode)
		newNode.setParent(p)

def getParameterNodes(n):
	# Returns the parameter leafs for the non-terminal symbol node n as
	# [[list of v1 nodes], [list of v2 nodes], ...]
	### !! VERY UNOPTIMIZED !! ###
	# Pretty sure it could be done in only one run 
	if n.getObject()[0] != "NT":
		return None # Not a "rule" node
	
	result = []
	argLabels = n.getObject()[3]
	for l in argLabels:
		result.append(getNodesWithLabel(n, l))
		
	return result

def getNodesWithLabel(n, label):
	# Returns a list of all nodes with the same object[1] (label) as label 
	result = []
	r_getNodesWithLabel(n, label, result)
	return result

def r_getNodesWithLabel(n, label, result):
	# Recursive call for getNodesWithLabel()
	if n.getObject()[1] == label:
		result.append(n)
	for nn in n.getChilds():
		r_getNodesWithLabel(nn, label, result)

def printTree(tree, t = 0):
	if (tree == None):
		print("Empty tree")
		return
		
	if (t > 0):
		print("\t" * (t) + "L" + str(tree.getObject()) + ("O" if tree.isMarked() else ""))
	else:
		print(str(tree.getObject()) + ("O" if tree.isMarked() else "")) 
	
	for c in tree.getChilds():
		printTree(c, t = t + 1)