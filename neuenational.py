from larlib import *

""" Mura Pianoterra """

filename = "pianoterra.lines"
lines_pt = lines2lines(filename)
pianoterra = STRUCT(AA(POLYLINE)(lines_pt))
VIEW(pianoterra)

V,EV = lines2lar(lines_pt) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.07))

pianoterra1D=V,EV

""" Qua ci devo mette la trasform1azione di scala """

""" Divido i muri di altezza diversa """
stairsEdges = [48,21,142,45,85,43,75,55,24,37,59,118,19,83,12,41,97,29] ##spigoli elle ringhiere delle scale
lines_stairs = [[V[EV[e][0]],V[EV[e][1]]] for e in stairsEdges]
ductsEdges = [60,7,98,138,10,13,149,77] ##spigoli dei condotti dell'aria
panelsEdges = [84,109,31,34,89,81,16,11,124,128,25,120,69,88,100,96,15,40,113,39,125,82,6,148,134,114] ##spigoli dei pannelli
wallsEdges = set(range(len(EV))).difference(panelsEdges+ductsEdges+stairsEdges)

""" Faccio l'OFFSET """
stairsHPCs = STRUCT(AA(POLYLINE)(lines_stairs))
ductsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in ductsEdges]))
panelsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in panelsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))
stairs = COLOR(RED)(OFFSET([.0025,.0025])(stairsHPCs))
ducts = COLOR(GREEN)(OFFSET([.01,.01])(ductsHPCs))
panels = COLOR(YELLOW)(OFFSET([.005,.005])(panelsHPCs))
walls = COLOR(CYAN)(OFFSET([.0025,.0025])(wallsHPCs))
##VIEW(STRUCT([ stairs,panels,walls,ducts ]))

"""Estrusione delle mura piano terra"""
stairsExtr = PROD([ STRUCT([stairs]), INTERVALS(0.009)(1) ])
ductsExtr = PROD([ STRUCT([ducts]), INTERVALS(0.14)(1) ])
panelsExtr = PROD([ STRUCT([panels]), INTERVALS(0.05)(1) ]) ###mettere altezza reale pannelli
wallsExtr = PROD([ STRUCT([walls, ducts]), INTERVALS(0.14)(1) ])
VIEW(STRUCT([panelsExtr, wallsExtr, ductsExtr, stairsExtr]))


"""Coloriamo le facce"""
##colors = [CYAN,MAGENTA,WHITE,RED,YELLOW,GREEN,GRAY,ORANGE, BLACK,BLUE,PURPLE,BROWN]
##VIEW(STRUCT([COLOR(colors[k%12])(cell) for k,cell in enumerate( MKTRIANGLES((V,FV,EV))) ]))

""" Costruzione della struttra di travi del tetto tramite pyplasm """
Y,FY = larCuboids([18,18])
Y,EY = larCuboidsFacets([Y,FY])
Y=(mat(Y)*3.56).tolist()
Y=(mat(Y)+[.31,.31]).tolist()
#VIEW(STRUCT(MKPOLS([Y,EY])))
beamsGrid = OFFSET([.3,.3])(STRUCT(MKPOLS([Y,EY])))
beamsHPC = PROD([ STRUCT([beamsGrid]), INTERVALS(1.8)(1) ])
beamsHPC = T(3)(.05)(beamsHPC)
#VIEW(beamsHPC)

""" Costruzione della copertura del tetto """
C,FC = larCuboids([1,1])
C = (mat(C)*65).tolist()
cover = larModelProduct([[C,FC],larQuote1D([.05])])
C,FC = cover
CT = (mat(C)+[0,0,1.85]).tolist()
coverHPC = COLOR(RED)(STRUCT(MKPOLS([CT,FC])))
#VIEW(coverHPC)
#VIEW(STRUCT([coverHPC,beamsHPC]))

""" Costruzione della base del tetto """
B,FB = larCuboids([18,18])
B,EB = larCuboidsFacets([B,FB])
B = (mat(B)*3.577777).tolist()
roofBase = OFFSET([.6,.6])(STRUCT(MKPOLS([B,EB])))
roofBaseHPC = COLOR(BLUE)(PROD([ STRUCT([roofBase]), INTERVALS(.05)(1) ]))
roof = STRUCT([roofBaseHPC,coverHPC,beamsHPC])
VIEW(roof)
