#! /usr/bin/python

from larlib import *

""" Costruzione della struttra di travi del tetto tramite pyplasm """
Y,FY = larCuboids([18,18])
Y,EY = larCuboidsFacets([Y,FY])
Y=(mat(Y)*3.577).tolist()
Y=(mat(Y)+[.107,.107]).tolist()
#VIEW(STRUCT(MKPOLS([Y,EY])))
beamsGrid = OFFSET([.25,.25])(STRUCT(MKPOLS([Y,EY])))
beamsHPC = PROD([ STRUCT([beamsGrid]), INTERVALS(1.8)(1) ])
beamsHPC = T(3)(8.65)(beamsHPC)
#VIEW(beamsHPC)

""" travi sottili """
U,FU = larCuboids([18,18])
U,EU = larCuboidsFacets([U,FU])
U=(mat(U)*3.597).tolist()
boundaryEdges = boundaryCells(FU,EU)
EU = [EU[i] for i in set(range(len(EU))).difference(boundaryEdges)]
thinGrid = OFFSET([.1,.1])(STRUCT(MKPOLS([U,EU])))
thin = COLOR(GRAY)(PROD([ STRUCT([thinGrid]), INTERVALS(1.8)(1) ]))
thin = T(3)(8.65)(thin)

""" Costruzione della copertura del tetto """
C,FC = larCuboids([1,1])
C = (mat(C)*64.85).tolist()
cover = larModelProduct([[C,FC],larQuote1D([.1])])
C,FC = cover
CT = (mat(C)+[0,0,10.45]).tolist() ##lo traslo di 10.25 ovvero 8.4 delle mura + 1.85 lo s spessore del muro
coverHPC = COLOR(GRAY)(STRUCT(MKPOLS([CT,FC])))
#VIEW(coverHPC)
#VIEW(STRUCT([coverHPC,beamsHPC]))

""" Costruzione della base del tetto """
B,FB = larCuboids([18,18])
B,EB = larCuboidsFacets([B,FB])
B = (mat(B)*3.575).tolist()
roofBase = OFFSET([.5,.5])(STRUCT(MKPOLS([B,EB])))
roofBaseHPC = COLOR(GRAY)(PROD([ STRUCT([roofBase]), INTERVALS(.05)(1) ]))
roofBaseHPC = T(3)(8.6)(roofBaseHPC) ##8.4 + l'offset su y del telaio

""" griglia interna """
V,FV = larCuboids([8,8])
V,EV = larCuboidsFacets([V,FV])
trasl = 2*3.577 +.25 + .107
V = (mat(V)*.405).tolist()
V = (mat(V) + [trasl,trasl]).tolist()
##VIEW(STRUCT(MKPOLS((V,EV))))
smallGrid = T(3)(8.75)(STRUCT(MKPOLS((V,EV))))
smallGrid = OFFSET([.05,.05,.05])(smallGrid)
grid = STRUCT(NN(14)([smallGrid,T(1)((8*.416)+.25)]))
grid = STRUCT(NN(14)([grid,T(2)((8*.416)+.25)]))
##VIEW(grid)

roof = STRUCT([roofBaseHPC,coverHPC,beamsHPC,thin,grid])

""" Mura Pianoterra """

filename = "pianoterra.lines"
lines_pt = lines2lines(filename)
V,EV = lines2lar(lines_pt) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.07))

""" trasform1azione di scala """
assert EV[32] == (30,69) ##spigolo di un muro del pianoterra. 30 e 69 sono i vertici
assert V[30],V[69] == ([7.146513749511273, 7.251609539945262], [57.54651374951127, 7.251609539945262])
V = ((mat(V) - [V[111][0],V[46][1]]) * (50.3/(V[69][0]-V[30][0]))).tolist() ##voglio allineare i pilastri in modo corretto e i vertici 8 e 4 sono quelli che prendo per trovare il vettore di traslazione su x e y

""" Divido i muri di altezza diversa """
stairsEdges = [4,8,3,84,51,136,73,21,123,116,87,113,5,125,27,127,2,107] ##spigoli elle ringhiere delle scale
lines_stairs = [[V[EV[e][0]],V[EV[e][1]]] for e in stairsEdges]
ductsEdges = [91,25,78,126,24,26,95,89] ##spigoli dei condotti dell'aria
panelsEdges = [63,10,47,40,58,131,9,17,75,142,132,59,129,114,12,94,33,104,151,46,39,14,134,64,77,147] ##spigoli dei pannelli
wallsEdges = [32,61,106,45]
pillarsEdges = set(range(len(EV))).difference(panelsEdges+ductsEdges+stairsEdges+wallsEdges)

""" Faccio l'OFFSET """
pillarsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in pillarsEdges]))
stairsHPCs = STRUCT(AA(POLYLINE)(lines_stairs))
ductsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in ductsEdges]))
panelsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in panelsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))
pillars = COLOR(BLACK)(OFFSET([.25,.25])(pillarsHPCs))
stairs = COLOR(RED)(OFFSET([.025,.025])(stairsHPCs))
ducts = COLOR(GREEN)(OFFSET([.5,.5])(ductsHPCs))
panels = COLOR(YELLOW)(OFFSET([.25,.25])(panelsHPCs))
walls = COLOR(CYAN)(OFFSET([.02,.02])(wallsHPCs))
##VIEW(STRUCT([ stairs,panels,walls,ducts,pillars ]))

"""Estrusione delle mura piano terra"""
pillarsE = PROD([ pillars, INTERVALS(8.4)(1) ])
stairsE = PROD([ stairs, INTERVALS(0.9)(1) ])
ductsE = PROD([ ducts, INTERVALS(8.4)(1) ])
panelsE = PROD([ panels, INTERVALS(4.4)(1) ]) ###mettere altezza reale pannelli
wallsE = PROD([ walls, INTERVALS(8.4)(1) ])
##VIEW(STRUCT([pillarsE,panelsE, wallsE, ductsE, stairsE]))

""" Costruzione del telaio """
lines = lines2lines("telaiopt.lines")
H,FH,EH,poly = larFromLines(lines)
HH = AA(LIST)(range(len(H)))
##VIEW(larModelNumbering(1,1,1)(H,[HH,EH,FH],STRUCT(MKPOLS([H,EH])),0.1)) 
H = (mat(H)-H[60]).tolist()
sx = 50.15/H[53][0]; sy = 8.4/H[53][1]
scaling = mat([[sx,0,0],[0,sy,0]])
H = ( mat(H)*scaling ).tolist()

vetriHPC = STRUCT(MKPOLS((H,FH)))
##VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS([H,FH])))
vetri = T(3)(0.075)(OFFSET([0.0,0.0,0.03])(vetriHPC))
telaioHPC = STRUCT(MKPOLS([H,EH]))
telaioN = STRUCT([vetri,COLOR(GRAY)(OFFSET([0.1,0.2,0.25])(telaioHPC))])
telaioN = R([2,3])(PI/2)(telaioN) ##mi sposto su x,z in modo da "estrudere" su y
telaioS = telaioO = telaioN
telaioS = T([1,2])([0.25,50.25])(telaioS)
telaioO = R([1,2])(PI/2)(telaioO)

lines = lines2lines("telaiopt2.lines")
H,FH,EH,poly = larFromLines(lines)
HH = AA(LIST)(range(len(H)))
##VIEW(larModelNumbering(1,1,1)(H,[HH,EH,FH],STRUCT(MKPOLS([H,EH])),0.1)) 
H = (mat(H)-H[20]).tolist()
sx = 50.15/H[80][0]; sy = 8.4/H[80][1]
scaling = mat([[sx,0,0],[0,sy,0]])
H = ( mat(H)*scaling ).tolist()

vetriHPC = STRUCT(MKPOLS((H,FH)))
##VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS([H,FH])))
vetri = T(3)(0.11)(OFFSET([0.0,0.0,0.03])(vetriHPC))
doorsEdges = [43,69,35,12,67,4,109,40,102,28]
doorsHPC = STRUCT(MKPOLS([H,[EH[i] for i in doorsEdges]]))
talaioEdges = set(range(len(EH))).difference(doorsEdges)
telaioHPC = STRUCT(AA(POLYLINE)([[H[EH[e][0]],H[EH[e][1]]] for e in talaioEdges]))
doors = OFFSET([0.2,0.25,0.25])(doorsHPC)
telaioE = OFFSET([0.1,0.2,0.25])(telaioHPC)
telaioE = STRUCT([COLOR(GRAY)(STRUCT([doors,telaioE])),vetri])
telaioE = R([2,3])(PI/2)(telaioE)
telaioE = T([1,2])([50.25,-0.05])(R([1,2])(PI/2)(telaioE))

telaio = STRUCT([telaioN,telaioE,telaioO,telaioS])
telaio = T([1,2])(SUM([[7.132334158738434, 7.237221425778705],[0,.25]]))(telaio) ##V[30]= [7.132334158738434, 7.237221425778705] (v30 e' il vertice in basso a sinistra delle mura)

"""Visualizzazione Pianoterra completo"""
pianoterra = STRUCT([pillarsE,panelsE, telaio, ductsE, stairsE,roof])
VIEW(pianoterra)

""" Creazione mura seminterrato """
filename = "seminterrato.lines"
lines_ps = lines2lines(filename)
V,EV = lines2lar(lines_ps) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.04))

""" Traslazione nell'origine e scalamento """
V = ((mat(V) - V[355])*108).tolist()
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,5))

""" Separazione tipi di muro """
#TODO: separazione spigoli
tallWallsEdges = [227,91,380,9,268,391,326,241,262,103,128,214,313,187,244,312,73,179,165]
wallsEdges = set(range(len(EV))).difference(tallWallsEdges)

tallWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in tallWallsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))

""" Faccio l'OFFSET """
#semint = OFFSET([.5,.5])(STRUCT(MKPOLS((V,EV))))
semint = OFFSET([.5,.5])(wallsHPCs)
tallWalls = COLOR(CYAN)(OFFSET([.5,.5])(tallWallsHPCs))

""" Estrusione mura """
semint = PROD([ semint, INTERVALS(4)(1) ])
tallWalls = T(3)(-2.5)(PROD([ tallWalls, INTERVALS(6.5)(1) ]))

""" Creazione colonne piccole """
def createColumns(repetitions, distance, scale):
	tx,ty = distance
	P,FP = larCuboids([1,1])
	P,EP = larCuboidsFacets([P,FP])
	P = (mat(P)*scale).tolist()
	O=P;EO=EP;FO=FP
	for i in range(repetitions - 1):
		X = (mat(P) + [ tx*(i+1) ,0 ]).tolist()
		EX = [SUM([EP[z],[4*(i+1),4*(i+1)]]) for z in range(len(EP))]
		FX = [[FP[0][u]+(4*(i+1)) for u in range(4)]]
		O = O+X
		EO = EO+EX
		FO = FO+FX
	P=O;EP=EO;FP=FO
	for i in range(repetitions - 1):
		X = (mat(O)+ [0, ty*(i+1)]).tolist()
		P=P+X
		EX = [SUM([EO[z],[48*(i+1),48*(i+1)]]) for z in range(len(EO))]
		EP=EP+EX
		FX = [[FP[w][u]+(48*(i+1)) for u in range(4)] for w in range(len(FO))]
		FP=FP+FX
	return P,FP,EP
	
C,FC = larCuboids([1,1])
C = ((mat(C)*.5)+ [(V[367][0]+1.4),7.4]).tolist()
columns = PROD([ STRUCT(MKPOLS((C,FC))), INTERVALS(4)(1) ])
colonne = STRUCT(NN(12)([columns,T(1)(7.2)]))
colonne = STRUCT(NN(12)([colonne,T(2)(7.2)]))

""" Creazione colonne grandi """
##colonne grandi verticali
C,FC = larCuboids([1,1])
C = (mat(C)+ [61.1,21.1216]).tolist()
columnsBV = [C,FC]
colonneGV = STRUCT(NN(2)([STRUCT(MKPOLS(columnsBV)),T(1)(28.8)]))
colonneGV = STRUCT(NN(2)([colonneGV,T(2)(64.8)]))
#colonne grandi orizontali
C,FC = larCuboids([1,1])
C = (mat(C)+ [43.1,39.1216]).tolist()
columnsBO = [C,FC]
colonneGO = STRUCT(NN(2)([STRUCT(MKPOLS(columnsBO)),T(2)(28.8)]))
colonneGO = STRUCT(NN(2)([colonneGO,T(1)(64.8)]))

colonneGV = PROD([ colonneGV, INTERVALS(4)(1) ])
colonneGO = PROD([ colonneGO, INTERVALS(4)(1) ])
colonneG = STRUCT([colonneGO,colonneGV])

""" Pavimento del Seminterrato """
lines = lines2lines("pavimento-semint.lines")
W,FW,EW,poly = larFromLines(lines)
WW = AA(LIST)(range(len(W)))
submodel = STRUCT(MKPOLS((W,EW)))
##VIEW(larModelNumbering(1,1,1)(W,[WW,EW,FW],submodel,0.07))
W = ((mat(W) - W[1])*108).tolist()

floors = (W,[FW[k] for k in range(len(FW)) if k!=5 and k!=4])
lower_floors = DIFFERENCE([STRUCT(MKPOLS([W,FW])),STRUCT(MKPOLS(floors))])
lower_floors = T(3)(-2.5)(PROD([ (lower_floors), INTERVALS(.1)(1) ]))
muri_dietro_scale = OFFSET([.3,0])(STRUCT(MKPOLS((W,[EW[5],EW[15]])))) ##muri sotto le scale
muri_dietro_scale = T(3)(-2.5)(PROD([muri_dietro_scale, INTERVALS(2.5)(1) ]))
regular_floors = PROD([STRUCT(MKPOLS(floors)), INTERVALS(.1)(1) ])
VIEW(STRUCT([regular_floors,lower_floors,muri_dietro_scale]))
