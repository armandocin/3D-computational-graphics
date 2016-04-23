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
ductsEdges = [] ##spigoli dei condotti dell'aria
panelsEdges = (V,[EV[k] for k in []]) ##spigoli dei pannelli
wallsEdges = set(range(len(EV))).difference(panelsEdges)

""" Faccio l'OFFSET """
ductsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in ductsEdges]))
panelsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in panelsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))
ducts = COLOR(GREEN)(OFFSET([.0025,.0025])(ductsHPCs))
panels = COLOR(YELLOW)(OFFSET([.0025,.0025])(panelsHPCs))
walls = COLOR(CYAN)(OFFSET([.005,.005])(wallsHPCs))

"""Estrusione delle mura piano terra"""
VIEW(STRUCT([ panels, walls ,ducts]))
panelsExtr = PROD([ STRUCT([panels]), INTERVALS(2)(1) ]) ###mettere altezza reale pannelli
wallsExtr = PROD([ STRUCT([walls, ducts]), INTERVALS(8.4)(1) ])
VIEW(STRUCT([panelsExtr, wallsExtr]))


"""Coloriamo le facce"""
##colors = [CYAN,MAGENTA,WHITE,RED,YELLOW,GREEN,GRAY,ORANGE, BLACK,BLUE,PURPLE,BROWN]
##VIEW(STRUCT([COLOR(colors[k%12])(cell) for k,cell in enumerate( MKTRIANGLES((V,FV,EV))) ]))

""" Costruzione della struttra di travi del tetto tramite pyplasm """
##domain2D = PROD([INTERVALS(64.8)(18), INTERVALS(64.8)(18)])
##domain3D = PROD([domain2D,INTERVALS(1.8)(1)])
##VIEW(SKEL_1(domain3D))
T,FT = larCuboids([18,18])
T,ET = larCuboidsFacets([T,FT])
T=(mat(T)*3.56).tolist()
T=(mat(T)+[.31,.31]).tolist()
VIEW(STRUCT(MKPOLS([T,ET])))
beamsGrid = OFFSET([.3,.3])(STRUCT(MKPOLS([T,ET])))
beams = COLOR(GRAY)(PROD([ STRUCT([beamsGrid]), INTERVALS(1.8)(1) ])) ##larModelProduct([roof,larQuote1D([1.8])])
VIEW(beams)

""" Costruzione della copertura del tetto """
C,FC = larCuboids([1,1])
C = (mat(C)*65).tolist()
cover = larModelProduct([[C,FC],larQuote1D([.05])])
C,FC = cover
CT = (mat(C)+[0,0,1.8]).tolist()
coverHPC = COLOR(RED)(STRUCT(MKPOLS([CT,FC])))
VIEW(coverHPC)
VIEW(STRUCT([coverHPC,beams]))

""" Costruzione della base del tetto """
