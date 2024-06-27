import copy
import random
from math import sqrt
#from geopy.distance import geodesic

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

    def buildGraph(self, colore, anno):
        self.graph.clear()
        nodi = DAO.getProdotti(colore)
        for i in nodi:
            self.graph.add_node(i)
            self.idMap[i.number] = i
        archi = DAO.getArchi(colore, anno)
        for a in archi:
            self.graph.add_edge(self.idMap[a[0]], self.idMap[a[1]], weight = a[2])
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:3]

    def cercaCammino(self, partenza):
        self.solBest = []
        parziale = [self.idMap[partenza]]
        self.ricorsione(parziale, self.idMap[partenza])
        return self.solBest

    def ricorsione(self, parziale, nodo):
        vicini = list(self.graph.neighbors(nodo))
        viciniAmmissibili = self.viciniAccettabili(parziale, vicini)
        if len(viciniAmmissibili) == 0 and len(parziale)>len(self.solBest):
            self.solBest = copy.deepcopy(parziale)
        else:
            for v in viciniAmmissibili:
                if self.vincoli(parziale, v):
                    parziale.append(v)
                    self.ricorsione(parziale, v)
                    parziale.pop()



    def viciniAccettabili(self, parziale, vicini):
        ammissibili= []
        if len(parziale)>1:
            for v in vicini:
                if self.graph[parziale[-2]][parziale[-1]]["weight"] < self.graph[parziale[-1]][v]["weight"]:
                    ammissibili.append(v)
        else:
            ammissibili= copy.deepcopy(vicini)
        return ammissibili

    def vincoli(self, parziale, v):
        if len(parziale) == 1:
            return True
        elif self.graph[parziale[-2]][parziale[-1]]["weight"]<self.graph[parziale[-1]][v]["weight"]:
            return True
        else:
            return False


    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)
