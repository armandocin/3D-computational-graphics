from larlib import *

""" Mura Pianoterra """

filename = "pianoterra.lines"
lines_pt = lines2lines(filename)
pianoterra = STRUCT(AA(POLYLINE)(lines_pt))
##VIEW(pianoterra)

V,EV = lines2lar(lines_pt) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
##VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.07))

""" trasform1azione di scala """
assert EV[77] == (88,141) ##spigolo di un muro del pianoterra. 88 e 141 sono i vertici
assert V[88],V[141] == ([0.1215, 0.1201], [0.8786, 0.1201])
## lo spigolo 77 è lungo 0.8786-0.1215 = 0.7536 e deve diventare di 50.4. Il fattore di scala è quindi 50.4/0.7536=66.88
V = ((mat(V) - [V[8][0],V[4][1]]) * (50.4/0.7536)).tolist() ##voglio allineare i pilastri in modo corretto e i vertici 8 e 4 sono quelli che prendo per trovare il vettore di traslazione su x e y

""" Divido i muri di altezza diversa """
stairsEdges = [106,53,41,25,60,51,58,94,115,40,71,92,43,131,134,133,19,75] ##spigoli elle ringhiere delle scale
lines_stairs = [[V[EV[e][0]],V[EV[e][1]]] for e in stairsEdges]
ductsEdges = [5,3,107,122,38,50,144,64] ##spigoli dei condotti dell'aria
panelsEdges = [82,147,28,65,132,127,104,9,4,12,24,54,14,45,21,129,143,111,83,105,73,72,89,16,23,84] ##spigoli dei pannelli
wallsEdges = [26,119,79,77]
pillarsEdges = set(range(len(EV))).difference(panelsEdges+ductsEdges+stairsEdges+wallsEdges)

""" Faccio l'OFFSET """
pillarsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in pillarsEdges]))
stairsHPCs = STRUCT(AA(POLYLINE)(lines_stairs))
ductsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in ductsEdges]))
panelsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in panelsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))
pillars = COLOR(BLACK)(OFFSET([.2,.2])(pillarsHPCs))
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
wallsE = PROD([ STRUCT([walls, ducts]), INTERVALS(8.4)(1) ])
##VIEW(STRUCT([pillarsE,panelsE, wallsE, ductsE, stairsE]))

"""Coloriamo le facce"""
##colors = [CYAN,MAGENTA,WHITE,RED,YELLOW,GREEN,GRAY,ORANGE, BLACK,BLUE,PURPLE,BROWN]
##VIEW(STRUCT([COLOR(colors[k%12])(cell) for k,cell in enumerate( MKTRIANGLES((V,FV,EV))) ]))

""" Costruzione della struttra di travi del tetto tramite pyplasm """
Y,FY = larCuboids([18,18])
Y,EY = larCuboidsFacets([Y,FY])
Y=(mat(Y)*3.63).tolist()
Y=(mat(Y)+[.285,.285]).tolist()
#VIEW(STRUCT(MKPOLS([Y,EY])))
beamsGrid = OFFSET([.3,.3])(STRUCT(MKPOLS([Y,EY])))
beamsHPC = PROD([ STRUCT([beamsGrid]), INTERVALS(1.8)(1) ])
beamsHPC = T(3)(8.45)(beamsHPC)
#VIEW(beamsHPC)

Y,FY = larCuboids([18,18])
Y,EY = larCuboidsFacets([Y,FY])
Y=(mat(Y)*3.67).tolist()
##YY = AA(LIST)(range(len(Y)))
##VIEW(larModelNumbering(1,1,1)(Y,[YY,EY],STRUCT(MKPOLS([Y,EY])),1))
d = [1,38,75,112,149,186,223,260,297,334,371,408,445,482,519,556,593,630,628,591,554,517,480,443,406,369,332,295,258,221,184,147,110,73]
thinEdges = set(range(len(EY))).difference(d+[i for i in range(37) if i%2==0]+[i for i in range(665,684)])
thinHPC = STRUCT(AA(POLYLINE)([[Y[EY[e][0]],Y[EY[e][1]]] for e in thinEdges]))
thinGrid = OFFSET([.15,.15])(thinHPC)
thin = COLOR(BLACK)(PROD([ STRUCT([thinGrid]), INTERVALS(1.8)(1) ]))
thin = T(3)(8.45)(thin)

""" Costruzione della copertura del tetto """
C,FC = larCuboids([1,1])
C = (mat(C)*66.21).tolist()
cover = larModelProduct([[C,FC],larQuote1D([.05])])
C,FC = cover
CT = (mat(C)+[0,0,10.25]).tolist() ##lo traslo di 10.25 ovvero 8.4 delle mura + 1.85 lo s spessore del muro
coverHPC = COLOR(RED)(STRUCT(MKPOLS([CT,FC])))
#VIEW(coverHPC)
#VIEW(STRUCT([coverHPC,beamsHPC]))

""" Costruzione della base del tetto """
B,FB = larCuboids([18,18])
B,EB = larCuboidsFacets([B,FB])
B = (mat(B)*3.645).tolist()
roofBase = OFFSET([.6,.6])(STRUCT(MKPOLS([B,EB])))
roofBaseHPC = COLOR(BLUE)(PROD([ STRUCT([roofBase]), INTERVALS(.05)(1) ]))
roofBaseHPC = T(3)(8.4)(roofBaseHPC)
roof = STRUCT([roofBaseHPC,coverHPC,beamsHPC,thin])
VIEW(STRUCT([pillarsE, panelsE, wallsE, ductsE, stairsE,roof]))