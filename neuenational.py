#! /usr/bin/python

from larlib import *

""" Costruzione della struttra di travi del tetto tramite pyplasm """
V=[[0,0],[0,64.85]]
EV = [[0,1]]
basetrave = OFFSET([.5,0])(STRUCT(MKPOLS([V,EV])))
#VIEW(basetrave)
basetrave = STRUCT(NN(2)([PROD([OFFSET([.5,0])(STRUCT(MKPOLS([V,EV]))),INTERVALS(.05)(1)]),T(3)(1.8)]))
centrotrave = T(1)(.2)(PROD([OFFSET([.1,0])(STRUCT(MKPOLS([V,EV]))),INTERVALS(1.8)(1)]))
#VIEW(STRUCT([basetrave,centrotrave]))
trave = STRUCT([basetrave,centrotrave])
traviX = STRUCT(NN(19)([trave,T(1)(3.575)]))
traviY = T(1)(64.85)(R([1,2])(PI/2)(traviX))
beams = T(3)(8.6)(STRUCT([traviY,traviX]))

""" Costruzione della copertura del tetto """
C,FC = larCuboids([1,1])
C = (mat(C)*64.85).tolist()
cover = larModelProduct([[C,FC],larQuote1D([.1])])
C,FC = cover
CT = (mat(C)+[0,0,10.45]).tolist() ##lo traslo di 10.25 ovvero 8.4 delle mura + 1.85 lo s spessore del muro
coverHPC = COLOR(GRAY)(STRUCT(MKPOLS([CT,FC])))
#VIEW(coverHPC)
#VIEW(STRUCT([coverHPC,beamsHPC]))

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

roof = STRUCT([beams,coverHPC,grid])

""" Mura Pianoterra """

filename = "pianoterra.lines"
lines_pt = lines2lines(filename)
V,EV = lines2lar(lines_pt) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.07))

""" trasform1azione di scala """
assert EV[32] == (30,69) ##spigolo di un muro del pianoterra. 30 e 69 sono i vertici
assert V[30],V[69] == ([0.1155, 0.1169], [0.8828, 0.1169])
V = ((mat(V) - [V[111][0],V[46][1]]) * (50.3/(V[69][0]-V[30][0]))).tolist() ##voglio allineare i pilastri in modo corretto e i vertici 8 e 4 sono quelli che prendo per trovare il vettore di traslazione su x e y

""" Divido i muri di altezza diversa """
stairsEdges = [4,8,3,84,51,136,73,21,123,116,87,113,5,125,27,127,2,107] ##spigoli elle ringhiere delle scale
lines_stairs = [[V[EV[e][0]],V[EV[e][1]]] for e in stairsEdges]
ductsEdges = [91,25,78,126,24,26,95,89] ##spigoli dei condotti dell'aria
panelsEdges = [63,10,47,40,58,131,9,17,75,142,132,59,129,114,12,94,33,104,151,46,39,14,134,64,77,147] ##spigoli dei pannelli
wallsEdges = [32,61,106,45]
pillarsEdges = set(range(len(EV))).difference(panelsEdges+ductsEdges+stairsEdges+wallsEdges)
#pt = (V,[EV[k] for k in panelsEdges+ductsEdges+stairsEdges+wallsEdges])

""" pilastri """
lines = lines2lines("pilastri.lines")
P,EP = lines2lar(lines)
#VIEW(larModelNumbering(1,1,1)(P,[AA(LIST)(range(len(P))),EP],STRUCT(MKPOLS((P,EP))),0.01))
P = ((mat(P) - [P[18][0],P[48][1]])*(50.3/(0.8828-0.1155))).tolist()

""" Faccio l'OFFSET """
#pillarsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in pillarsEdges]))
pillarsHPCs = STRUCT(MKPOLS((P,EP)))
stairsHPCs = STRUCT(AA(POLYLINE)(lines_stairs))
ductsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in ductsEdges]))
panelsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in panelsEdges]))
#wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))
pillars = COLOR(BLACK)(OFFSET([.05,.05])(pillarsHPCs))
stairs = COLOR(RED)(OFFSET([.025,.025])(stairsHPCs))
ducts = COLOR(GREEN)(OFFSET([.5,.5])(ductsHPCs))
panels = COLOR(YELLOW)(OFFSET([.25,.25])(panelsHPCs))
#walls = COLOR(CYAN)(OFFSET([.02,.02])(wallsHPCs))
##VIEW(STRUCT([ stairs,panels,walls,ducts,pillars ]))

"""Estrusione delle mura piano terra"""
pillarsE = PROD([ pillars, INTERVALS(8.35)(1) ])
stairsE = PROD([ stairs, INTERVALS(0.9)(1) ])
ductsE = PROD([ ducts, INTERVALS(8.4)(1) ])
panelsE = PROD([ panels, INTERVALS(4.4)(1) ]) ###mettere altezza reale pannelli
#wallsE = PROD([ walls, INTERVALS(8.4)(1) ])
##VIEW(STRUCT([pillarsE,panelsE, wallsE, ductsE, stairsE]))

C,FC = larCuboids([3,1])
C,EC = larCuboidsFacets([C,FC])
#VIEW(larModelNumbering(1,1,1)(C,[AA(LIST)(range(len(C))),EC,FC],STRUCT(MKPOLS((C,EC))),0.7))
scaling = mat([[1.1570376645379952/3,0,0],[0,0.38021634302098306,0]])
C = (mat(C)*scaling).tolist()
cross2 = OFFSET([.05,.05,.05])(STRUCT(MKPOLS((C,FC))))
cross2 = R([1,2])(-PI/2)(STRUCT(MKPOLS((C,FC))))
cross2 = T([1,2])([0.38841066075850605,0.38841066075850605+0.38021634302098306])(cross2)
cross = STRUCT([STRUCT(MKPOLS((C,FC))),cross2])
cross = OFFSET([.05,.05,.05])(cross)
cyl1 = T(3)(.07)(CYLINDER([.16,.06])(100))
cyl2 = T(3)(.13)(CYLINDER([.22,.07])(100))
cyl3 = CYLINDER([.22,.07])(100)
cyl = STRUCT([cyl1,cyl2,cyl3])
cyl = T([1,2,3])([1.1570376645379952/2,0.38021634302098306/2,.05])(cyl)
top = STRUCT([cyl,cross])
tops = STRUCT([T([1,2])(P[k])(top) for k in [34,54,9,96,60,99,37,91]])
tops = T(3)(8.35)(tops)
pillarsE = STRUCT([tops, pillarsE])

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
pianoterra = T([1,2,3])([43.5,21.7,5.5])(STRUCT([pillarsE,panelsE, telaio, ductsE, stairsE,roof]))
#VIEW(pianoterra)

""" Creazione mura seminterrato """
filename = "mura-semint.lines"
lines_ps = lines2lines(filename)
V,EV = lines2lar(lines_ps) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.04))

""" Traslazione nell'origine e scalamento """
V = ((mat(V) - V[299])*108).tolist()
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,5))

""" Separazione tipi di muro """
#TODO: separazione spigoli
tallWallsEdges = [254,95,140,265,151,7,42,292,274,167,117,244,153,323,296,99,284,271,213,133,315,31]
thickWallsEdges = [66,86,17,134,98,138,58,14,23,175,37,306,142,162,145,260,233,21,236,191,65,108,74,83,12,160,41,169,203,280,18,245,222,27,131,239,127,78,55,310,120,320,261,10,157,132,47,43,221,154,252,46,0,49,170,130,90,29,228]
wallsEdges = set(range(len(EV))).difference(tallWallsEdges+[328]+thickWallsEdges) #328 spigolo che devo sostituire con la vetrata

tallWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in tallWallsEdges]))
thickWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in thickWallsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))

""" Faccio l'OFFSET """
walls = OFFSET([.3,.3])(wallsHPCs)
tallWalls = COLOR(CYAN)(OFFSET([.5,.5])(tallWallsHPCs))
thickWalls = COLOR(GREEN)(OFFSET([.5,.5])(thickWallsHPCs))

""" Estrusione muri """
walls = PROD([ walls, INTERVALS(4)(1) ])
tallWalls = T(3)(-2.5)(PROD([ tallWalls, INTERVALS(6.5)(1) ]))
thickWalls = PROD([ thickWalls, INTERVALS(4)(1) ])

""" Creazioni pannelli seminterrato """
filename = "pannelli-semint.lines"
lines_ps = lines2lines(filename)
U,EU = lines2lar(lines_ps) ##creo Vertici e Spigoli del piano terra
UU = AA(LIST)(range(len(U)))
submodel = STRUCT(MKPOLS((U,EU)))
##VIEW(larModelNumbering(1,1,1)(U,[UU,EU],submodel,0.04))
assert U[45][0] - U[57][0] == 0.1061
U = ((mat(U) - U[57])*(8.7372/0.1061)).tolist()
U = (mat(U) + [23.6088, 21.481199999999998]).tolist()
basementPanels =  COLOR(YELLOW)(OFFSET([.2,.2])(STRUCT(MKPOLS([U,EU]))))
basementPanels = PROD([ basementPanels, INTERVALS(3)(1) ])

basementWalls = STRUCT([walls, thickWalls, basementPanels,tallWalls])

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

C,FC,EC = createColumns([12,12],[7.2,7.2],.5)
C = (mat(C)+ [(V[309][0]+1.4),7.4]).tolist()
#CC = AA(LIST)(range(len(C)))
#VIEW(larModelNumbering(1,1,1)(C,[CC,EC,FC],STRUCT(MKPOLS((C,EC))),0.1))
tallColumns = (C,[FC[k] for k in [112,113,124,125,40,41,52,53]])
regularColumns = (C, [FC[k] for k in set(range(len(FC))).difference([112,113,124,125,40,41,52,53])])
tallColumnsHPCs = T(3)(-2.4)(PROD([ STRUCT(MKPOLS(tallColumns)), INTERVALS(6.5)(1) ]))
regularColumnsHPCs = PROD([ STRUCT(MKPOLS(regularColumns)), INTERVALS(4)(1) ])
smallColumns = STRUCT([regularColumnsHPCs,tallColumnsHPCs])
#C,FC = larCuboids([1,1])
#C = ((mat(C)*.5)+ [(V[367][0]+1.4),7.4]).tolist()
#columns = PROD([ STRUCT(MKPOLS((C,FC))), INTERVALS(4)(1) ])
#colonne = STRUCT(NN(12)([columns,T(1)(7.2)]))
#colonne = STRUCT(NN(12)([colonne,T(2)(7.2)]))
	
""" Creazione colonne grandi """
##colonne grandi verticali
C,FC = larCuboids([1,1])
C = (mat(C)+ [61.1,21.1216]).tolist()
columnsBV = [C,FC]
bigColumnsVertical = STRUCT(NN(2)([STRUCT(MKPOLS(columnsBV)),T(1)(28.8)]))
bigColumnsVertical = STRUCT(NN(2)([bigColumnsVertical,T(2)(64.8)]))
#colonne grandi orizontali
C,FC = larCuboids([1,1])
C = (mat(C)+ [43.1,39.1216]).tolist()
columnsBO = [C,FC]
bigColumnsOriz = STRUCT(NN(2)([STRUCT(MKPOLS(columnsBO)),T(2)(28.8)]))
bigColumnsOriz = STRUCT(NN(2)([bigColumnsOriz,T(1)(64.3)]))

bigColumnsVertical = PROD([ bigColumnsVertical, INTERVALS(4)(1) ])
bigColumnsOriz = PROD([ bigColumnsOriz, INTERVALS(4)(1) ])
bigColumns = STRUCT([bigColumnsOriz,bigColumnsVertical])

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
muri_dietro_scale = OFFSET([.3,0])(STRUCT(MKPOLS((W,[EW[5],EW[15]])))) ##muri dietro le scale
muri_dietro_scale = T(3)(-2.5)(PROD([muri_dietro_scale, INTERVALS(2.5)(1) ]))
regular_floors = PROD([STRUCT(MKPOLS(floors)), INTERVALS(.1)(1) ])
basementFloors = STRUCT([regular_floors,lower_floors,muri_dietro_scale])

""" Costruzione telaio e vetrata seminterrato """
lines = lines2lines("telaio-semint.lines")
P,FP,EP,polygons = larFromLines(lines)
#VIEW(larModelNumbering(1,1,1)(P,[AA(LIST)(range(len(P))),EP,FP],STRUCT(MKPOLS((P,EP))),0.1))
P = (mat(P)-P[71]).tolist()
sx = 93.4328/P[2][0]; sy = 3.75/P[2][1]
scaling = mat([[sx,0,0],[0,sy,0]])
P = ( mat(P)*scaling ).tolist()

glassWallsHPC = STRUCT(MKPOLS((P,FP)))
glassWalls = T(3)(0.11)(OFFSET([0.0,0.0,0.03])(glassWallsHPC))
frame = OFFSET([.2,.25,.25])(STRUCT(MKPOLS([P,EP])))
frameAndWindows = R([2,3])(PI/2)(STRUCT([COLOR(GRAY)(frame),glassWalls]))
frameAndWindows = T([1,2])([20.4,94.1328])(R([1,2])(-PI/2)(frameAndWindows))

seminterrato = STRUCT([basementFloors,frameAndWindows,basementWalls,bigColumns,smallColumns])
#VIEW(STRUCT([basementFloors,frameAndWindows,basementWalls,bigColumns,smallColumns]))

""" Costruzione pavimento podio/tetto seminterrato """
lines = lines2lines("tetto-semint.lines")
U,FU,EU,poly = larFromLines(lines)
#VIEW(larModelNumbering(1,1,1)(U,[AA(LIST)(range(len(U))),EU,FU],STRUCT(MKPOLS((U,EU))),5))

U = (mat(U)-U[10]).tolist()
U = ((mat(U)*(94.1328/U[9][1]))+ [20, 0.0]).tolist()

staircase1 = (U,[FU[k] for k in range(9)])
upFloorHPC = DIFFERENCE([STRUCT(MKPOLS((U,FU))), STRUCT(MKPOLS(staircase1))])
#VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS(staircase1)))

upFloor = OFFSET([.3,.3])(upFloorHPC)
upFloor = T(3)(4)(PROD([upFloor, INTERVALS(1.5)(1)]))

W,FW = staircase1

stairsmodel = SKEL_1(STRUCT(MKPOLS((W,FW))))
VIEW(larModelNumbering(1,1,1)(W,[AA(LIST)(range(len(W))),FW],stairsmodel,2))
FW = sorted(FW,key=lambda cell: CCOMB([W[k] for k in cell])[0]) #Riordino le facce delle scale
stairsmodel = SKEL_1(STRUCT(MKPOLS((W,FW))))
VIEW(larModelNumbering(1,1,1)(W,[AA(LIST)(range(len(W))),FW],stairsmodel,2))
"""
staircase1struct = Struct([([W[k] for k in cell],[range(len(cell))]) for cell in [FW[i] for i in range(8)]]) 
scalinata1 = embedStruct(1)(staircase1struct)
staircase1 = CAT(DISTL([t(0,0,-(2*0.16)),scalinata1.body]))
staircase1 = struct2lar(Struct(staircase1))
VIEW(STRUCT(MKPOLS(staircase1)))
lastStep = (W,[FW[8]])
lastStep = T(3)(-1.5)(PROD([STRUCT(MKPOLS(lastStep)), INTERVALS(0.06)(1)]))
staircase1 = larModelProduct([staircase1,larQuote1D([0.16])])
"""
step = OFFSET([.0375,0])(STRUCT(MKPOLS((W,[FW[0]]))))
step = T(3)(5.32)(PROD([step,INTERVALS(.18)(1)]))
steps = STRUCT(NN(8)([ step, T([1,3])([1.0755,-0.18]) ]))
lastStep = OFFSET([.3,0])(STRUCT(MKPOLS((W,[FW[8]]))))
lastStep = T(3)(4)(PROD([lastStep, INTERVALS(0.06)(1)]))

sx = U[4][0]-U[7][0]
sy = U[7][1]-U[8][1]
tri = SIMPLEX(2)
rampa = T(2)(1)(R([2,3])(PI/2)(PROD([tri,INTERVALS(1)(1)])))
rampa = S([1,2,3])([sx,sy,1.5])(rampa)
rampa = T([1,2,3])([U[8][0],U[8][1],4])(rampa)
staircase1 = STRUCT([lastStep,steps,rampa])

VIEW(STRUCT([basementFloors,frameAndWindows,basementWalls,bigColumns,smallColumns, staircase1,upFloor]))

""" Creazione cornicione del podio """
lines = lines2lines("cornicione.lines")
Z,EZ = lines2lar(lines)
#VIEW(larModelNumbering(1,1,1)(Z,[AA(LIST)(range(len(Z))),EZ,FZ],STRUCT(MKPOLS((Z,EZ))),5))
Z = (mat(Z)-Z[19]).tolist()
Z = ((mat(Z)*(94.1328/Z[17][1]))+ [19.8, -.2]).tolist()

cornicione = OFFSET([.2,.2])(STRUCT(MKPOLS((Z,EZ))))
cornicione = T(3)(5.5)(PROD([cornicione, INTERVALS(.5)(1)]))
