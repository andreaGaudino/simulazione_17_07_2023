import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None



    def load_interface(self):
        # title
        self._title = ft.Text("simulazione esame 24/01/2024", color="blue", size=24)
        self._page.controls.append(self._title)

        #row1
        self.ddAnno = ft.Dropdown(label="Anno")
        self.ddColore = ft.Dropdown(label="Colore")
        self.btnCreaGrafo = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([ft.Container(self.ddAnno, width=300),
                       ft.Container(self.ddColore, width=300),
                       ft.Container(self.btnCreaGrafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #row2
        self.ddPartenza = ft.Dropdown(label="Vertice di partenza")
        self.btnCammino = ft.ElevatedButton(text="Cerca cammino", on_click=self._controller.handleCammino)
        row2 = ft.Row([ft.Container(self.ddPartenza, width=300),
                       ft.Container(self.btnCammino, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txtResGrafo = ft.ListView(expand=1)
        row3 = ft.Row([self.txtResGrafo])
        self._page.controls.append(row3)

        self.txtArchi = ft.ListView(expand=1)
        row4 = ft.Row([self.txtArchi])
        self._page.controls.append(row4)

        self._controller.fillDD()

        self.txtCammino = ft.ListView(expand=1)
        row5 = ft.Row([self.txtCammino])
        self._page.controls.append(row5)
        self._page.update()
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
