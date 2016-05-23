from larlib import *

""" Creazione colonne piccole """
def createColumns(repetitionsXY, traslationXY, scale=1):
	tx,ty = traslationXY
	rx,ry = repetitionsXY
	P,FP = larCuboids([1,1])
	P,EP = larCuboidsFacets([P,FP])
	P = (mat(P)*scale).tolist()
	O=P;EO=EP;FO=FP
	for i in range(rx - 1):
		X = (mat(P) + [ tx*(i+1) ,0 ]).tolist()
		EX = [SUM([EP[z],[4*(i+1),4*(i+1)]]) for z in range(len(EP))]
		FX = [[FP[0][u]+(4*(i+1)) for u in range(4)]]
		O = O+X
		EO = EO+EX
		FO = FO+FX
	P=O;EP=EO;FP=FO
	for i in range(ry - 1):
		X = (mat(O)+ [0, ty*(i+1)]).tolist()
		P=P+X
		EX = [SUM([EO[z],[(4*rx)*(i+1),(4*rx)*(i+1)]]) for z in range(len(EO))]
		EP=EP+EX
		FX = [[FP[w][u]+((4*rx)*(i+1)) for u in range(4)] for w in range(len(FO))]
		FP=FP+FX
	return P,FP,EP

def createFilledSteps(N,dimensioni):
    sx,sy,sz = dimensioni
    V,FV=larCuboids([1,1])
    step = S([1,2])([sx,sy])(STRUCT(MKPOLS((V,FV))))
    step =  steps = PROD([step,INTERVALS(sz)(1)])
    for i in range(1,N):
        stepp = T(3)(-sz*i)(S(1)(1+i)(step))
        steps = STRUCT([steps,stepp])
    return steps

def createSteps(N,dimensioni,underStairs=False):
    sx,sy,sz = dimensioni
    V,FV=larCuboids([1,1])
    step = S([1,2])([sx,sy])(STRUCT(MKPOLS((V,FV))))
    step =  steps = PROD([step,INTERVALS(sz)(1)])
    steps = STRUCT(NN(N)([step, T([1,3])([sx,-sz])]))
    if(underStairs==True):
		base=CUBOID([sx*(N-1),sy,sz])
		m=MAT([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,-(sz*N)*1./(sx*N),0,1]])
		filled=m(base)	   
		return STRUCT([filled,steps])	
    return steps
