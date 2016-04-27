from larlib import *

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
pillarsE = PROD([ STRUCT([pillars]), INTERVALS(8.4)(1) ])
stairsE = PROD([ STRUCT([stairs]), INTERVALS(0.9)(1) ])
ductsE = PROD([ STRUCT([ducts]), INTERVALS(8.4)(1) ])
panelsE = PROD([ STRUCT([panels]), INTERVALS(2.5)(1) ]) ###mettere altezza reale pannelli
wallsE = PROD([ STRUCT([walls]), INTERVALS(8.4)(1) ])
##VIEW(STRUCT([pillarsE,panelsE, wallsE, ductsE, stairsE]))

""" Costruzione del telaio """
lines = lines2lines("telaiopt.lines")
H,EH = lines2lar(lines)
HH = AA(LIST)(range(len(H)))
##VIEW(larModelNumbering(1,1,1)(H,[HH,EH],STRUCT(MKPOLS([H,EH])),0.1)) 
H = (mat(H)-H[72]).tolist()
sx = 50.4/H[54][0]; sy = 8.4/H[54][1]
scaling = mat([[sx,0,0],[0,sy,0]])
H = ( mat(H)*scaling ).tolist()

telaioHPC = STRUCT(MKPOLS([H,EH]))
telaioN = OFFSET([0.1,0.2,0.05])(telaioHPC)
telaioN = R([2,3])(PI/2)(telaioN) ##mi sposto su x,z in modo da "estrudere" su y
telaioS = telaioO = telaioN
telaioS = T([1,2])([0.05,50.5])(telaioS)
telaioO = R([1,2])(PI/2)(telaioO)

lines = lines2lines("telaiopt2.lines")
H,EH = lines2lar(lines)
HH = AA(LIST)(range(len(H)))
##VIEW(larModelNumbering(1,1,1)(H,[HH,EH],STRUCT(MKPOLS([H,EH])),0.1)) 
H = (mat(H)-H[84]).tolist()
sx = 50.4/H[65][0]; sy = 8.4/H[65][1]
scaling = mat([[sx,0,0],[0,sy,0]])
H = ( mat(H)*scaling ).tolist()

doorsEdges = [41,33,39,13,67,4,110,27,123,38]
doorsHPC = STRUCT(MKPOLS([H,[EH[i] for i in doorsEdges]]))
talaioEdges = set(range(len(EH))).difference(doorsEdges)
telaioHPC = STRUCT(AA(POLYLINE)([[H[EH[e][0]],H[EH[e][1]]] for e in talaioEdges]))
doors = OFFSET([0.2,0.25,0.05])(doorsHPC)
telaioE = OFFSET([0.1,0.2,0.05])(telaioHPC)
telaioE = (STRUCT([doors,telaioE])
telaioE = R([2,3])(PI/2)(telaioE)
telaioE = T([1,2])([50.5,-0.05])(R([1,2])(PI/2)(telaioE))

telaio = COLOR(BLACK)(STRUCT([telaioN,telaioE,telaioO,telaioS]))
telaio = T([1,2])(V[30])(telaio)

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

Y,FY = larCuboids([18,18])
Y,EY = larCuboidsFacets([Y,FY])
Y=(mat(Y)*3.597).tolist()
##YY = AA(LIST)(range(len(Y)))
##VIEW(larModelNumbering(1,1,1)(Y,[YY,EY],STRUCT(MKPOLS([Y,EY])),1))
d = [1,38,75,112,149,186,223,260,297,334,371,408,445,482,519,556,593,630,628,591,554,517,480,443,406,369,332,295,258,221,184,147,110,73]
thinEdges = set(range(len(EY))).difference(d+[i for i in range(37) if i%2==0]+[i for i in range(665,684)])
thinHPC = STRUCT(AA(POLYLINE)([[Y[EY[e][0]],Y[EY[e][1]]] for e in thinEdges]))
thinGrid = OFFSET([.1,.1])(thinHPC)
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
roof = STRUCT([roofBaseHPC,coverHPC,beamsHPC,thin])

pianoterra = STRUCT([pillarsE,panelsE, telaio, ductsE, stairsE,roof])
VIEW(pianoterra)
