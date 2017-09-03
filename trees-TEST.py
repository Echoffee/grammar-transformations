from trees import *
import copy
# Arbre root = 
#		 root
#      /     \
#     f       h
#   /  \    /  \
#  a   g   f   a
#      |  / \
#      b a  a 


root = node(None)
obj_root = ["NT", "root", 2, ["a", "b"]]	# [type]
obj_f = ["T", "f", 2, []]
obj_g = ["T", "g", 1, []]
obj_h = ["T", "h", 2, []]
obj_a = ["P", "a", 0, []]
obj_b = ["P", "b", 0, []]
root.setObject(obj_root)


#First line
f1 = node(root)
f1.setObject(obj_f)
h1 = node(root)
h1.setObject(obj_h)

#Second line
a21 = node(f1)
a21.setObject(obj_a)
g2 = node(f1)
g2.setObject(obj_g)

f2 = node(h1)
f2.setObject(obj_f)
a22 = node(h1)
a22.setObject(obj_a)

#Third line
b3 = node(g2)
b3.setObject(obj_b)
a31 = node(f2)
a31.setObject(obj_a)
a32 = node(f2)
a32.setObject(obj_a)

###############################################################

# Try to find a f(a, a) sub-tree in t1 :
def test1():
	t1 = copy.deepcopy(root)
	pattern1 = node(None)
	pattern1.setObject(obj_f)
	pa1 = node(pattern1)
	pa2 = node(pattern1)
	pa1.setObject(obj_a)
	pa2.setObject(obj_a)
	sn = findPattern(t1, pattern1)
	printTree(sn)

###############################################################
# Try to find a g(b) sub-tree in t1 :
def test2():
	t1 = copy.deepcopy(root)
	pattern1 = node(None)
	pattern1.setObject(obj_g)
	pb1 = node(pattern1)
	pb1.setObject(obj_b)
	sn = findPattern(t1, pattern1)
	printTree(sn)

###############################################################
# Try to find a g sub-tree in t1 :
def test25():
	t1 = copy.deepcopy(root)
	pattern1 = node(None)
	pattern1.setObject(obj_g)
	sn = findPattern(t1, pattern1)
	printTree(sn)

###############################################################
# Try to find a f(b, a) sub-tree in t1 (doesn't exist):
def test3():
	t1 = copy.deepcopy(root)
	pattern1 = node(None)
	pattern1.setObject(obj_f)
	pb1 = node(pattern1)
	pb1.setObject(obj_b)
	pb2 = node(pattern1)
	pb2.setObject(obj_a)
	sn = findPattern(t1, pattern1)
	printTree(sn)
	
###############################################################
# Replace a nodes by g(a) sub-trees:
def test4():
	t1 = copy.deepcopy(root)
	pb1 = node(None)
	pb1.setObject(obj_a)
	p = node(None)
	p.setObject(obj_g)
	p2 = node(p)
	p2.setObject(obj_a)
	replaceInTree(t1, [p])
	printTree(t1)

###############################################################
# Find all of the f() sub-trees in t1:
def test5():
	t1 = copy.deepcopy(root)
	p1 = node(None)
	p1.setObject(obj_f)
	sn = findPatterns(t1, p1)
	print(sn)
	printTree(t1)
	

#############################################################
# Trees :
# X =       X
#         /  
#        f   
#      /  \
#    v2    f
#         / \
#        v1  v1
# 
# Y =       Y
#         /  \ 
#        f    b
#      /  \
#     v   f
#		 / \
#       u   u

obj_xroot = ["NT", "X", 2, ["v1", "v2"]]
obj_yroot = ["NT", "Y", 0, []]
obj_f = ["S", "f", 2, []]
obj_u = ["S", "u", 0, []]
obj_v = ["S", "v", 0, []]
obj_b = ["S", "b", 0, []]
obj_v1 = ["P", "v1", 0, []]
obj_v2 = ["P", "v2", 0, []]
xroot = node(None)
xroot.setObject(obj_xroot)
xl = node(xroot)
xl.setObject(obj_f)
xll = node(xl)
xll.setObject(obj_v2)
xlr = node(xl)
xlr.setObject(obj_f)
xlrl = node(xlr)
xlrl.setObject(obj_v1)
xlrr = node(xlr)
xlrr.setObject(obj_v1)

yroot = node(None)
yroot.setObject(obj_yroot)
yl = node(yroot)
yl.setObject(obj_f)
yll = node(yl)
yll.setObject(obj_v)
ylr = node(yl)
ylr.setObject(obj_f)
ylrl = node(ylr)
ylrl.setObject(obj_u)
ylrr = node(ylr)
ylrr.setObject(obj_u)
yr = node(yroot)
yr.setObject(obj_b)

################################################################
# Look for X sub-trees in Y 
def test6():
	tx = copy.deepcopy(xroot)
	ty = copy.deepcopy(yroot)
	r = findPatternWithParams(ty, tx)
	printTree(r[0])
	
