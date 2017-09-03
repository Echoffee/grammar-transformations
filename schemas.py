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
				i = self.parseRule(nn, e, i+1, root)
			elif e[i] == ')' or e[i] == '+':
				nn = node(n)
				lll = list(filter(lambda x : x[0] == w, self.RS))
				a = lll[0][1] if len(lll) > 0 else [0, []]
				nn.setObject(["S", w, a[0], a[1]])
				w = ""
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
						else:
							nnn = node(None)
							t = "S"
							if ccn in root.getObject()[3]:
								t = "P"
							nnn.setObject([t, ccn, 0])
							nnn.setParent(n)
							nC = nC + [nnn]
				
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
		
		self.generateTree()
			
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
	
	def GT_IntroductionRandom(self):
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
		l = list(filter(lambda x : x[2] > 0, ng.RS))
		ll = ng.RS
		for a in args_s:
			ll = ll + [["P", a[0], 0, []]]
			
		for j in range(plus_count):
			f = random.choice(l)
			n = node(root)
			n.setObject(f)
			ng.r_randomizeRules(n, 0, ll)
		
		r = [func_s[0], func_s[1], arg_string, ng.rewriteRules(root, 1)]
		ng.R = ng.R + [r]
		ng.generateTree()
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
		
	def GT_DeleteUnused(self):
		# Delete all of the unused rules in the grammar
		u = self.getUnusedRules()
		for n in u:
			l = list(filter(lambda x : x.getObject()[1] == n[0], self.T))
			for ll in l:
				self.T.remove(l)
			
			self.R.remove(n)
			
	def GT_DeleteUnusedRandom(self):
		# Delete a random rule from the unused ones
		u = self.getUnusedRules()
		n = random.choice(u)
		l = list(filter(lambda x : x.getObject()[1] == n[0], self.T))
		for ll in l:
			self.T.remove(ll)
		
		self.R.remove(n)
		
	def getUnusedRules(self):
		result = []
		for r in self.R:
			n = node(None)
			obj_r = ["S", r[0], r[1], r[2]]
			n.setObject(obj_r)
			unused = True
			for t in list(filter(lambda x : x.getObject()[1] != r[0], self.T)):
				if findPattern(t, n) != None:
					unused = False
			
			if unused:
				result = result + [r]
		
		return result

def printGramTree(g):
	print("Symbols :")
	print(str(g.getSymbols()))
	print("\nRules :")
	for gg in g.getRules():
		print(gg)
