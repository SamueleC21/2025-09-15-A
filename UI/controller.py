import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno1 = None
        self._anno2 = None


    def handleCreaGrafo(self,e):
        self._view.txt_result.clean()
        if self._anno1 is None or self._anno2 is None:
            self._view.txt_result.controls.append(ft.Text("Inserire anni", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(self._anno1, self._anno2)
        self._view.txt_result.controls.append(ft.Text(f"grafdo creato correttamente con"
                                                      f"{len(self._model._graph.nodes)} nodi e {len(self._model._graph.edges)} archi", color="green"))

        self._view.update_page()


    def handleDettagli(self, e):
        edgesBest = self._model.getEdgesBest()
        self._view.txt_result.controls.append(ft.Text("i tre archi con peso maggiore sono: "))
        for e in edgesBest:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} --> {e[1]} con peso di {e[2]["weight"]}"))
        self._view.update_page()

        self._view.txt_result.controls.append(ft.Text(f"le componeneti connesse sono {self._model.numCompCon()}"))
        self._view.update_page()
        nodiBigger = self._model.nodiCompConnBigger()
        self._view.txt_result.controls.append(ft.Text(f"i tre nodi della componenete connessa maggiore sono: "))
        for n in nodiBigger:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleCerca(self, e):
        pass


    def fillDD(self):
        anni = self._model.getYears()
        for anno in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(data=anno, key=anno, on_click=self.readAnno1))
            self._view._ddAnno2.options.append(ft.dropdown.Option(data=anno, key=anno, on_click=self.readAnno2))


    def readAnno1(self,e):
        self._anno1 = int(e.control.data)

    def readAnno2(self,e):
        self._anno2 = int(e.control.data)