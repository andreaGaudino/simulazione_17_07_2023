import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDD(self):
        anni = [2015, 2016, 2017, 2018]
        anniDD = list(map(lambda x: ft.dropdown.Option(x), anni))
        self._view.ddAnno.options = anniDD

        colori = DAO.getColori()
        coloriDD = list(map(lambda x: ft.dropdown.Option(x), colori))
        self._view.ddColore.options = coloriDD

        self._view.update_page()

    def handleCreaGrafo(self, e):
        self.anno = self._view.ddAnno.value
        if self.anno is None:
            self._view.create_alert("Anno non inserito")
            self._view.update_page()
            return

        self.colore = self._view.ddColore.value
        if self.colore is None:
            self._view.create_alert("Colore non inserito")
            self._view.update_page()
            return
        bestArchi = self._model.buildGraph(self.colore, self.anno)

        n, e = self._model.graphDetails()
        self._view.txtResGrafo.controls.append(ft.Text(f"Grafo creato con {n} nodi e {e} archi"))
        self._view.update_page()

        ripetuti = {}
        for i in bestArchi:
            self._view.txtArchi.controls.append(ft.Text(f"{i[0]}, {i[1]} peso={i[2]}"))
            for j in i[:2]:
                if j not in ripetuti:
                    ripetuti[j] = 1
                else:
                    ripetuti[j] +=1
        res = []
        for r in ripetuti:
            if ripetuti[r] >1:
                res.append(r)
        self._view.txtArchi.controls.append(ft.Text(f"{res}"))
        self.fillDDNodo()
        self._view.update_page()


    def fillDDNodo(self):
        nodi = list(self._model.graph.nodes)
        nodiDD = list(map(lambda x:ft.dropdown.Option(text=x.name, key=x.number), nodi))
        self._view.ddPartenza.options = nodiDD
        self._view.update_page()

    def handleCammino(self, e):
        self.partenza = int(self._view.ddPartenza.value)
        if self.partenza is None:
            self._view.create_alert("Nodo di partenza non inserito")
            self._view.update_page()
            return
        soluzione = self._model.cercaCammino(self.partenza)
        self._view.txtCammino.controls.append(ft.Text(f"Cammino di lunghezza {len(soluzione)-1}"))
        for i in range(len(soluzione)-1):
            self._view.txtCammino.controls.append(ft.Text(f"{soluzione[i]} --> {soluzione[i+1]} peso:{self._model.graph[soluzione[i]][soluzione[i+1]]["weight"]}"))
        self._view.update_page()


