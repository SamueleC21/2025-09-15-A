from operator import gt

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._mappaP = {}


    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, anno1, anno2):
        self._graph.clear()
        anno1str = str(anno1) + "-01-01"
        anno2str = str(anno2) + "-12-31"
        self._nodiP = DAO.getPiloti(anno1str, anno2str)
        for p in self._nodiP:
            self._mappaP[p.driverId] = p
        self._graph.add_nodes_from(self._nodiP)
        self.addEdges(anno1str, anno2str)

    def addEdges(self, anno1, anno2):
        edges = DAO.getEdges(anno1, anno2, self._mappaP)
        for e in edges:
            self._graph.add_edge(e[0], e[1], weight=e[2])

    def getEdgesBest(self):
        #listaTupleEdges = []
        #for u, v, peso in self._graph.edges(data=True):
        #    listaTupleEdges.append((u,v, peso["weight"]))
        #listaTupleEdges.sort(key = lambda x: x[2], reverse=True)
        #return listaTupleEdges[:3]
        listaTuple = list(self._graph.edges(data=True))
        listaTuple.sort(key=lambda x: x[2]["weight"], reverse=True)
        return listaTuple[:3]

    def numCompCon(self):
        return len(list(nx.connected_components(self._graph)))

    def nodiCompConnBigger(self):
        num = self.numCompCon()
        posizione = 0
        valore = 0
        for i in range(num):
            comp = nx.connected_components(self._graph)[i]
            if len(comp) > valore:
                valore = len(comp)
                posizione = i
        compConnBigger = nx.connected_components(self._graph)[posizione]
        #compConnBigger.sort()
        return compConnBigger[:3]