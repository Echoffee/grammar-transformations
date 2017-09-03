from grammars import *
from strategies import *
from trees import *

import random, copy

class gramTree :
	def __init__(self, symbols = [], rules = []):
		super(gramTree, self).__init__()
		self.S = symbols
		self.R = rules
		self.Red = []
		self.T = []
		self.RS = []
		
		if self.R != []:
			for r in self.R:
				self.RS = self.RS + [["NT", r[0], r[1], []]]
		
		if self.S != []:
			for s in self.S:
				self.RS = self.RS + [["S", s[0], s[1], []]]
			
		# 	return
			# for r in self.R:
			# 	# node = treeNode([r[0], r[1], r[2]])
			# 	self.T = self.T + [node]
			# 	exp = r[3]
			# 	i = 0
			# 	while i < len(exp): 
			# 		i = self.parseRule(node, exp, i)
			# 		i = i + 1
		
	def getSymbols(self):
		return self.S
		
	def getRules(self):
		return self.R
			
	def getTrees(self):
		return self.T
	
	def generateTree(self):
		self.T = []
		for r in self.R:
			n = node(None)
			n.setObject(["NT", r[0], r[1], r[2].replace(" ", "").split(',')])
			self.T = self.T + [n]
			exp = r[3]
			i = 0
			while i < len(exp): 
				i = self.parseRule(n, exp, i, n)
				i = i + 1
		
	def parseRule(self, n, e, i, root):
		w = ""
		e = e.replace(" ", "")
		while i < len(e):
			if e[i] == '(':
				nn = node(n)
				lll = list(filter(lambda x : x[0] == w, self.RS))
				a = [lll[0][1], lll[0][2]] if len(lll) > 0 else [0, []]
				nn.setObject(["S", w, a[0], a[1]])
				w = ""
				# n.addNode(nn)
				i = self.parseRule(nn, e, i+1, root)
			elif e[i] == ')' or e[i] == '+':
				nn = node(n)
				lll = list(filter(lambda x : x[0] == w, self.RS))
				a = lll[0][1] if len(lll) > 0 else [0, []]
				nn.setObject(["S", w, a[0], a[1]])
				w = ""
				# n.addNode(nn)
				nC = []
				for cc in n.getChilds():
					strs = cc.getObject()[1].split(",")
					num = 0
					strs = list(filter(lambda x : len(x) > 0, strs))
					for ii in range(len(strs)):
						ccn = strs[ii]
						if (len(cc.getChilds()) > 0 and ii == len(strs) - 1) :
							nC = nC + [cc]
							cc.setObject([cc.getObject()[0], ccn, cc.getObject()[2]])
							# cc.O[0] = ccn
						else:
							nnn = node(None)
							t = "S"
							if ccn in root.getObject()[3]:
								t = "P"
							nnn.setObject([t, ccn, 0])
							nnn.setParent(n)
							nC = nC + [nnn]
				
				# n.C = nC
				n.setChilds(nC)
				return i 
			else:
				w = w + e[i]
			i = i + 1
		return i	
		
	def randomizeRules(self, count):
		#random generation with given symbols and number of rules
		func_symbols = ["A", "B", "C", "D", "E"]
		func_symbols_min = ["a", "b", "c", "d", "e"]
		args_symbols = ["v"]
		func_ss = []
		for i in range(count):
			func_ss = func_ss + [["NT", "" + func_symbols[i // len(func_symbols_min)] + func_symbols_min[i % len(func_symbols_min)], randint(1, 3)]]
			
		for i in range(count):
			func_s = func_ss[i]
			args_s = []
			arg_string = ""
			for ii in range(func_s[2]):
				a = random.choice(args_symbols) + str(ii + 1)
				args_s = args_s + [["P", a, 0, []]]
				if (ii != 0):
					arg_string = arg_string + ", "
					
				arg_string = arg_string + a
				
			root = node(None)
			root.setObject(func_s)
			# plus_count = randint(1, 3)
			plus_count = randint(1, 1)
			la = []
			for x in self.S:
				na = ["S", x[0], x[1], []]
				la = la + [na]
				
			self.RS =  args_s + la
			l = list(filter(lambda x : x[2] > 0, self.RS))
			self.RS = self.RS + func_ss
			for j in range(plus_count):
				f = random.choice(l)
				n = node(root)
				n.setObject(f)
				ll = self.RS
				self.r_randomizeRules(n, 0, ll)
				
			self.R = self.R + [[func_s[1], func_s[2], arg_string, self.rewriteRules(root, 1)]]
		
		#tree generation
		self.generateTree()
		# for r in self.R:
		# 	n = node(None)
		# 	n.setObject([r[0], r[1], r[2]])
		# 	self.T = self.T + [n]
		# 	exp = r[3]
		# 	i = 0
		# 	while i < len(exp): 
		# 		i = self.parseRule(n, exp, i)
		# 		i = i + 1
			
	def r_randomizeRules(self, nn, n, ll):
		for i in range(nn.getObject()[2]):
			l = ll #args
			if (n == 3): # max tree depth 
				#remove funcs & rules
				l = list(filter(lambda x : x[2] == 0, ll))
				
			f = random.choice(l)	#must also add rules & args
			ni = node(nn)
			ni.setObject(f)
			self.r_randomizeRules(ni, n + 1, ll)
			
	def rewriteRules(self, nn, root):
		s = ""
		if (root == 1):
			for i in range(len(nn.getChilds())):
				if (i != 0):
					s = s + " + "
				s = s + self.rewriteRules(nn.getChilds()[i], 0)
		else:
			if nn.getObject()[2] > 0:
				s = s + nn.getObject()[1] + "("
			else:
				s = nn.getObject()[1]
				return s
			for i in range(len(nn.getChilds())):
				if (i != 0):
					s = s + ", "
				s = s + self.rewriteRules(nn.getChilds()[i], 0)
			if nn.getObject()[2] > 0:
				s = s + ")"
		
		return s
			
	def getReducedGram(self):
		#How do I smile ?
		return gram(self.Red[0], self.Red[1], self.Red[2], self.Red[3], None)
	
	def reduce(self, axiom):
		axiom = next(filter(lambda x : x[0] == axiom, self.R))
		vs = axiom[2].replace(" ", "").split(",")
		GR = []
		for i in range(len(vs)):
			GR = GR + [["S_0", [axiom[0] + str(i + 1), vs[i]]]]

		allPaths = []
		GZ = ["S_0"]
		GX = []
		for n in self.T:
			P = []
			final = []
			n.paths([], P, final, 0)
			allPaths = allPaths + final

		for r in self.R:
			ll = r[2].replace(" ", "").split(",")
			for iii in range(len(ll)):
				v = ll[iii]
				rules = list(filter(lambda x : x[0][-1] == v and x[0][0] == r[0], allPaths))
				for ri in range(len(rules)):
					rules[ri][0] = rules[ri][0][2:-1]
					nr = []
					for ii in range(int(len(rules[ri][0])/2)):
						nr = nr + [rules[ri][0][2*ii] + str(rules[ri][0][2*ii+1])]
						
					rules[ri] = nr
					
				for vv in rules:
					GR = GR + [[r[0] + str(iii + 1), vv]]
					
		for vs in self.S:
			for i in range(vs[1]):
				GX.append(vs[0] + str(i + 1))
				
		for vr in self.R:
			for i in range(vr[1]):
				GZ.append(vr[0] + str(i + 1))
				
		rep = {}
		for v in GZ:
			rep[v] = v
			
		self.Red = [GZ, GX, GR, "S_0", rep]
	# 
	# def parseRule(self, n, e, i):
	# 	w = ""
	# 	e = e.replace(" ", "")
	# 	while i < len(e):
	# 		if e[i] == '(':
	# 			nn = treeNode([w, 0])
	# 			w = ""
	# 			n.addNode(nn)
	# 			i = self.parseRule(nn, e, i+1)
	# 		elif e[i] == ')' or e[i] == '+':
	# 			nn = treeNode([w, 0])
	# 			w = ""
	# 			n.addNode(nn)
	# 			nC = []
	# 			for cc in n.C:
	# 				strs = cc.O[0].split(",")
	# 				num = 0
	# 				strs = list(filter(lambda x : len(x) > 0, strs))
	# 				for ii in range(len(strs)):
	# 					ccn = strs[ii]
	# 					if (len(cc.C) > 0 and ii == len(strs) - 1) :
	# 						nC = nC + [cc]
	# 						cc.O[0] = ccn
	# 					else:
	# 						nC = nC + [treeNode([ccn, 0])]
	# 			
	# 			n.C = nC
	# 			return i 
	# 		else:
	# 			w = w + e[i]
	# 		i = i + 1
	# 	return i
	# 	
	
	def gt_random_introduction(self):
		ng = gramTree(self.getSymbols(), self.getRules())
		func_s = ["rule_" + str(len(self.R)), randint(1, 3)] # [rule name, number of params]
		args_s = []
		arg_string = ""
		for ii in range(func_s[1]):
			a = "v" + str(ii + 1)
			args_s = args_s + [[a, 0]]
			if (ii != 0):
				arg_string = arg_string + ", "
				
			arg_string = arg_string + a
			
			
		root = node(None)
		root.setObject(["NT", func_s[0], func_s[1], args_s])
		plus_count = randint(1, 3)	# Number of members (R = t1 + t2 + ...)
		#ng.RS = args_s + self.S
		l = list(filter(lambda x : x[2] > 0, ng.RS))
		#ng.RS = ng.RS + self.R
		ll = ng.RS
		for a in args_s:
			ll = ll + [["P", a[0], 0, []]]
			
		for j in range(plus_count):
			f = random.choice(l)
			n = node(root)
			n.setObject(f)
			# root.addNode(n)
			
			ng.r_randomizeRules(n, 0, ll)
		
		r = [func_s[0], func_s[1], arg_string, ng.rewriteRules(root, 1)]
		ng.R = ng.R + [r]
		ng.generateTree()
		# node = treeNode([r[0], r[1], r[2]])
		# ng.T = self.T + [node]
		# exp = r[3]
		# i = 0
		# while i < len(exp): 
		# 	i = ng.parseRule(node, exp, i)
		# 	i = i + 1
			
		return ng
		
	#deprecated
	def gt_random_unfold(self):
		#There is chances for the function doing nothing if the randomly chosen rule isn't used anywhere
		rule = random.choice(self.R)
		print("=== Chosen rule ===")
		print(rule)
		print("===================")
		rule_tree = random.choice(list(filter(lambda x : x.O[0] == rule[0], self.T)))
		ng = gramTree()
		ng.S = self.S
		ng.T = copy.deepcopy(self.T)
		rr = list(filter(lambda x : x.O[0] != rule[0], ng.T))
		for r in rr:
			self.gt_random_unfold_local_node(rule_tree, r)
		
		for n in ng.T:
			arg_string = ""
			args_s = []
			for ii in range(n.O[1]):
				a = "v" + str(ii + 1)
				args_s = args_s + [[a, 0]]
				if (ii != 0):
					arg_string = arg_string + ", "
					
				arg_string = arg_string + a
				
			ng.R = ng.R + [[n.getObject()[0], n.getObject()[1], arg_string, ng.rewriteRules(n, 1)]]
			
		return ng
		
	def GT_UnfoldRandom(self):
		rule = random.choice(self.R)
		print("=== Chosen rule ===")
		print(rule)
		print("===================")
		t = random.choice(list(filter(lambda x : x.getObject()[1] != rule[0], self.T))) # which rule to apply unfold
		print("=== Chosen tree ===")
		printTree(t)
		print("===================")
		t = self.GT_Unfold(rule[0], t)
		return t
	
	def GT_Unfold(self, rule, t):
		rule = next(filter(lambda x : x[0] == rule, self.R))
		rule_tree = next(filter(lambda x : x.getObject()[1] == rule[0], self.T))
		lr = getNodesWithLabel(t, rule[0])
		# Does not work properly for simultaneous recursive unfoldings (like R1 = R2(R2(a)))
		#for lrn in lr:
		if len(lr) > 0 :		# Only for tab convenience with previous commented line
			lrn = random.choice(lr)
			nn = copy.deepcopy(rule_tree)
			vnodes = getParameterNodes(nn)
			if vnodes == None :
				print("No node found")
				return
				
			for i in range(len(vnodes)):
				for vn in vnodes[i]:
					replaceInTree2(vn, lrn.getChilds()[i])
			
			# Skip the root node (rule itself)
			# IMPORTANT : Only take the first member of the unfolding rule (in case of R(A) = t1 + t2 + ..., R will be only unfolded as t1)
			replaceInTree2(lrn, nn.getChilds()[0])
		
		return t
		# patternToFind = node(None)
		# patternToFind.setObject(rule_tree.getObject())
		# t = random.choice(list(filter(lambda x : x.getObject()[1] != rule[0], self.T)))
		# nfo = findPattern(t, patternToFind)
		# rt2 = copy.deepcopy(rule_tree.getChilds()[0])
		# if (nfo != None):
		# 	print("before")
		# 	printTree(rt2)
		# 	replaceInTree(rt2, nfo.getChilds(), rule_tree.getObject()[3])
		# 	print("after")
		# 	printTree(rt2)
		# 	i = nfo.getParent().removeChild(nfo)
		# 	nfo.getParent().setChild(rt2, i)
		# else:
		# 	print("No node found")
		
	def gt_random_unfold_local_node(self, tr, n):
		if n.getObject()[0] == tr.getObject()[0]:
			args = copy.deepcopy(n.C)
			n.C = copy.deepcopy(tr.C)
			n.setObject(copy.deepcopy(tr.getObject()))
			a = tr.getObject()[2].replace(" ", '').split(',')
			n.replace_nodes_with_labels(a, args)
		else :
			for nn in n.C :
				self.gt_random_unfold_local_node(tr, nn)
			
		
################################################################################
################################################################################
# 
# class treeNode:
# 	def __init__(self, o):
# 		self.C = []	
# 		self.O = o
# 
# 	def addNode(self, n):
# 		self.C = self.C + [n]
# 
# 	def paths(self, s, P, final, branch):
# 		if (branch > 0):
# 			s = s + [branch] + [self.O[0]]
# 		else :
# 			s = s + [self.O[0]]
# 		if len(self.C) == 0:
# 			P = P + [s]
# 			final.append(P)
# 		else:
# 			for b in range(len(self.C)):
# 				self.C[b].paths(s, P, final, b + 1)
# 		
# 	def replace_nodes_with_labels(self, list_labels, list_nodes):
# 		if self.O[0] in list_labels :
# 			i = list_labels.index(self.O[0])
# 			self = copy.deepcopy(list_nodes[i])
# 		else:
# 			for n in self.C:
# 				n.replace_nodes_with_labels(list_labels, list_nodes)

def printGramTree(g):
	print("Symbols :")
	print(str(g.getSymbols()))
	print("\nRules :")
	for gg in g.getRules():
		print(gg)
################################################################################
################################################################################
# g = gramTree(
# [["h", 1], ["g", 2], ["f", 2]],
# [("phi", 2, "v1, v2", "h(v1) + g(v2, phi(v2, theta(v1, h(v2))))"),
# ("theta", 2, "v1, v2", "g(v2, phi(v2, v1)) + f(v2, theta(v1, v1))")])
# 
# # g.reduce("phi")
# # g2 = g.get_reduced_gram()
# # # print(g.Red)
# # g3 = greibach(productive(g2))
# # S=word_to_mat(["phi1"],g2)
# # T=word_to_mat(["phi2"],g2)
# #P=strategy_DCMA(g3,S,T)
# 
# gg = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
# gg.randomize(2)
# gg2 = gg.gt_random_unfold()
# gg.reduce("Aa")
# gg2.reduce("Aa")
# ggr = gg.get_reduced_gram()
# ggr2 = gg2.get_reduced_gram()
# # gg2 = gg.get_reduced_gram()
# print(gg.R)
# print("---")
# print(ggr)
# print("===============")
# print(gg2.R)
# print("---")
# print(ggr2)
