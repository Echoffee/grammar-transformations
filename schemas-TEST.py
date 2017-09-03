from schemas import *


######################################################
# Generate random grammar
def gtest1():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
	g.randomizeRules(3)
	printGramTree(g)
	printTree(g.getTrees()[0])


######################################################
# Generate random grammar + unfold
def gtest2():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
	g.randomizeRules(3)
	g.generateTree()
	t = g.GT_UnfoldRandom()
	printTree(t)

######################################################
# Generate tree on given grammar + unfold on selected rule
def gtest21():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [
	["Aa", 3, "v1, v2, v3", "g(f(v1, v1), Ab(v3, v1))"],
	["Ab", 2, "v1, v2", "g(f(Ab(v2, Ac(v2, v2, v2)), Aa(Ac(v2, v2, v2), v2, f(v2, v1))), Ab(Aa(v2, Ac(v2, v1, v1), Aa(v2, v1, v2)), h(f(v2, v1))))"]
	])
	g.generateTree()
	printTree(g.getTrees()[0])
	g.GT_Unfold("Ab")
	printTree(g.getTrees()[0])

######################################################
# Reduction on random grammar
def gtest3():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
	g.randomizeRules(3)
	g.generateTree()
	printGramTree(g)
	g.reduce("Aa")
	g2 = g.getReducedGram()
	print(g2)
	
######################################################
# Generate random grammar + intro
def gtest4():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
	g.randomizeRules(3)
	g.generateTree()
	printGramTree(g)
	ng = g.GT_IntroductionRandom()
	printGramTree(ng)

######################################################
# Generate random grammar + intro + suppr (intro'd)
def gtest5():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
	g.randomizeRules(3)
	g.generateTree()
	g = g.GT_IntroductionRandom()
	printGramTree(g)
	print("Unused rules :")
	print(g.getUnusedRules())
	g.GT_DeleteUnusedRandom()
	print("...")
	printGramTree(g)

######################################################
# Fold grammar (same example as in trees-TEST (6))
def gtest6():
	g = gramTree([["f", 2], ["g", 2]], [
	["X", 2, "v1, v2", "f(v2, f(v1, v1))"],
	["Y", 3, "u, v, b", "f(f(v, f(u, u)), b)"]
	])
	g.generateTree()
	printTree(g.getTrees()[0])
	printTree(g.getTrees()[1])
	g.GT_FoldFirstFound()
	print("After folding...")
	printTree(g.getTrees()[1])
	

######################################################
# Generate random grammar + unfold + (re)fold
def gtest7():
	g = gramTree([["h", 1], ["g", 2], ["f", 2]], [])
	g.randomizeRules(3)
	g.generateTree()
	t = g.GT_UnfoldRandom()
	printTree(t)
	g.GT_FoldFirstFound()
	printTree(t)
	
gtest7()