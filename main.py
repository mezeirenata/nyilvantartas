from os import system as cmd

cmd("pip install textual")
from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function
from textual.widgets import (
    Input,
    Label,
    Button,
    Header,
    Select,
    DataTable,
    Pretty,
    TextArea,
    Collapsible,
)
from textual.containers import Horizontal, Center, Vertical
from diak import *
from tanar import *
from opciok import *
from hazik import *

# tantárgyak listája
TARGYAK = list(diakok[0].jegyek)


# app
class KretaApp(App):

    CSS = """

    Input.-valid {
        border: tall $success 60%;
    }
    Input.-valid:focus {
        border: tall $success;
    }
    Input {
        width: 30%;
        margin-bottom: 2;
    }
    .centerCont {
        align: center middle;
    }
    .btn {
        text-style: none;
        margin: 3;
    }
    .loginLabel {
        margin: 2 3;
        color: auto;
        background: white 25%;
        padding: 1;
    }
    .label {
        margin-left: 3;
        margin-bottom: 1;
    }
    #diakJegyek {
        margin-top: 2;
        margin-left: 6;
        background: blue 30%;
        color: auto;
        padding: 1 3;
    }
    #diakJegyekSelect, #tanarHazikSelect {
        width: 35%;
        margin-left: 3;
        margin-bottom: 1;
    }
    #logoutBtn {
        background: red 60%;
        color: auto;
    }
    #tanarHazikArea {
        width: 50%;
        height: 10;
        margin-left: 3;
    }
    #tanarHaziView {
        overflow: auto;
    }
    #tanarHazikInputOsztaly {
        width: 15;
    }
    * {
        overflow: hidden;
    }
    .overflow {
        overflow: auto;
        border: round white;
    }
    #diakOrarend {
        margin-top: 1;
        margin-left: 3;
        border: round blue;
        width: 63%;
    }
    #diakHazik {
        margin-left: 3;
    }
    .btns, #loginScreen {
        border: round white;
    }
    .success {
        color: green;
    }
    .fail {
        color: red;
    }
    #tanarHazikSuccessLabel {
        margin-top: 1;
        margin-left: 3;
        margin-bottom: 8;
    }
    .hazik {
        margin-left: 4;
        margin-top: 1;
        width: 50%;
    }
    .screen {
        width: 35%;
    }
    """

    # globális email, jelszó változó
    global email
    global password
    email = ""
    password = ""

    # init widgets
    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(
            Vertical(Label("Üdvözöljük!"), classes="centerCont"),
            Vertical(
                Input(placeholder="Email", validators=[Function(bad_e)], id="email"),
                Input(
                    placeholder="Jelszó",
                    validators=[Function(bad_p)],
                    password=True,
                    id="password",
                ),
                classes="centerCont",
            ),
            Horizontal(
                Button(label="Bejelentkezés", id="loginBtn", classes="btn"),
                Button(label="Reset", id="resetBtn", classes="btn"),
                classes="centerCont",
            ),
            id="loginScreen",
        )

        # diák nézet
        yield Horizontal(
            Vertical(
                Button("Kijelentkezés", id="logoutBtn", classes="btn"),
                Label("", classes="loginLabel", id="diakLoginLabel"),
                Horizontal(
                    Button("Órarend", id="diakOrarendBtn", classes="btn"),
                    Button("Jegyek", id="diakJegyekBtn", classes="btn"),
                    Button("Házi feladatok", id="diakHaziBtn", classes="btn"),
                ),
                classes="btns screen",
            ),
            Vertical(
                Label("\nÓrarend", id="diakOrarendLabel", classes="label"),
                DataTable(id="diakOrarend", zebra_stripes=True),
                id="diakOrarendView",
                classes="overflow",
            ),
            Vertical(
                Label("", id="diakJegyekLabel", classes="label"),
                Select(
                    ((line, line) for line in TARGYAK),
                    id="diakJegyekSelect",
                    allow_blank=False,
                    value="Történelem",
                ),
                Label("", id="diakJegyek"),
                id="diakJegyekView",
                classes="overflow",
            ),
            Vertical(
                Label("\nHázi feladatok", id="diakHazikLabel", classes="label"),
                Label("", id="diakHazik"),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    Label("", classes="hazikContent"),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                id="diakHaziView",
                classes="overflow",
            ),
            id="diakScreen",
        )

        # tanár nézet
        yield Horizontal(
            Vertical(
                Button("Kijelentkezés", id="logoutBtn", classes="btn"),
                Label("", classes="loginLabel", id="tanarLoginLabel"),
                Horizontal(
                    Button("Házi feladatok", id="tanarHaziBtn", classes="btn"),
                    Button("Jegyek", id="tanarJegyekBtn", classes="btn"),
                ),
                Pretty("", id="targyak"),
                classes="btns screen",
            ),
            Vertical(
                Label("Órarend", id="tanarOrarendLabel", classes="label"),
                DataTable(id="tanarOrarend"),
                id="tanarOrarendView",
                classes="overflow",
            ),
            Vertical(
                Label("", id="tanarJegyekLabel", classes="label"),
                Label("", id="tanarJegyek"),
                id="tanarJegyekView",
                classes="overflow",
            ),
            Vertical(
                Label("", id="tanarHazikLabel", classes="label"),
                Input(
                    placeholder="Osztály",
                    validators=[Function(bad_class)],
                    id="tanarHazikInputOsztaly",
                    classes="label",
                ),
                Label("Tantárgy:", classes="label"),
                Select(
                    ((line, line) for line in TARGYAK),
                    id="tanarHazikSelect",
                    allow_blank=False,
                    value="Történelem",
                ),
                Label("Határidő:", classes="label"),
                Input(
                    placeholder="YYYY.HH.NN",
                    validators=[Function(date)],
                    id="tanarHazikInputHatar",
                    classes="label",
                    max_length=10,
                ),
                Label("Feladat:", classes="label"),
                TextArea(id="tanarHazikArea", soft_wrap=True, show_line_numbers=False),
                Horizontal(
                    Button("Feljegyzés", id="tanarHazikBtn", classes="btn"),
                    Button("Reset", id="tanarHazikBtnReset", classes="btn"),
                ),
                Label("", classes="label", id="tanarHazikSuccessLabel"),
                id="tanarHaziView",
                classes="overflow",
            ),
            id="tanarScreen",
        )

    def on_mount(self):
        self.query_one("#diakScreen").display = False
        self.query_one("#tanarScreen").display = False

        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakJegyekView").display = False
        self.query_one("#diakHaziView").display = False

        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarOrarendView").display = False
        self.query_one("#tanarJegyekView").display = False

        self.title = "Kréta 2.0"

    # handle button presses
    @on(Button.Pressed, "#resetBtn")
    def reset(self, event: Button.Pressed) -> None:
        self.query_one("#email").value = ""
        self.query_one("#password").value = ""

    @on(Button.Pressed, "#logoutBtn")
    def logout(self, event: Button.Pressed) -> None:
        self.query_one("#loginScreen").display = True
        self.query_one("#diakScreen").display = False
        self.query_one("#tanarScreen").display = False
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakJegyekView").display = False
        self.query_one("#diakHaziView").display = False
        self.query_one("#tanarOrarendView").display = False
        self.query_one("#tanarJegyekView").display = False
        self.query_one("#tanarHaziView").display = False

    @on(Button.Pressed, "#diakOrarendBtn")
    def diaOrarend(self, event: Button.Pressed) -> None:
        self.query_one("#diakOrarendView").display = True
        self.query_one("#diakHaziView").display = False
        self.query_one("#diakJegyekView").display = False

    @on(Button.Pressed, "#diakJegyekBtn")
    def diakJegyek(self, event: Button.Pressed) -> None:
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakHaziView").display = False
        self.query_one("#diakJegyekView").display = True

    @on(Button.Pressed, "#diakHaziBtn")
    def diakHazik(self, event: Button.Pressed) -> None:
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakHaziView").display = True
        self.query_one("#diakJegyekView").display = False

    @on(Button.Pressed, "#tanarOrarendBtn")
    def tanarOrarend(self, event: Button.Pressed) -> None:
        self.query_one("#tanarOrarendView").display = True
        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarJegyekView").display = False

    @on(Button.Pressed, "#tanarJegyekBtn")
    def tanarJegyek(self, event: Button.Pressed) -> None:
        self.query_one("#tanarOrarendView").display = False
        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarJegyekView").display = True

    @on(Button.Pressed, "#tanarHaziBtn")
    def tanarHazik(self, event: Button.Pressed) -> None:
        self.query_one("#tanarOrarendView").display = False
        self.query_one("#tanarHaziView").display = True
        self.query_one("#tanarJegyekView").display = False
        self.query_one("#tanarHazikSuccessLabel").display = False

    @on(Button.Pressed, "#tanarHazikBtn")
    def tanarHazikFeljegyzes(self, event: Button.Pressed) -> None:
        osztaly = self.query_one("#tanarHazikInputOsztaly").value
        targy = self.query_one("#tanarHazikSelect").value
        hatar = self.query_one("#tanarHazikInputHatar").value
        feladat = self.query_one("#tanarHazikArea").text
        label = self.query_one("#tanarHazikSuccessLabel")
        label.display = True
        if (osztaly != "") and (targy != "") and (hatar != "") and (feladat != ""):
            f = open("csv/hazik.csv", "a", encoding="utf-8")
            f.write(f"{osztaly}\n{targy}\n{hatar}\n{feladat}\nEND\n")
            f.close()
            label.update("Sikeres feljegyzés!")
            label.classes = "success"
        else:
            label.update("Sikertelen feljegyzés!\nTöltsön ki minden mezőt!")
            label.classes = "fail"

    @on(Button.Pressed, "#tanarHazikBtnReset")
    def tanarHazikFeljegyzesReset(self, event: Button.Pressed) -> None:
        self.query_one("#tanarHazikInputOsztaly").value = ""
        self.query_one("#tanarHazikSelect").value = "Történelem"
        self.query_one("#tanarHazikInputHatar").value = ""
        self.query_one("#tanarHazikArea").text = ""
        self.query_one("#tanarHazikSuccessLabel").update("")

    @on(Button.Pressed, "#loginBtn")
    def login(self, event: Button.Pressed) -> None:
        # diák bejelentkezés
        for d in diakok:
            if d.email == email and d.jelszo == password:
                self.query_one("#loginScreen").display = False
                self.query_one("#diakScreen").display = True

                self.query_one("#diakLoginLabel").update(
                    f"Bejelentkezve: {d.nev} (diák)\nOsztály: {d.osztaly}\n\nJelenlegi ösztöndíj: {d.osztondij}"
                )
                self.query_one("#diakJegyekLabel").update(
                    f"\nJegyek\n\nTanulmányi átlag: {d.tan_atlag:.2f}"
                )
                self.query_one("#diakJegyek").display = False
                table: DataTable = self.query_one("#diakOrarend")
                table.clear(True)
                table.add_columns(*d.orarend[0])
                table.add_rows(d.orarend[1:])

                for a in self.query(".hazik"):
                    a.display = False

                diakHazik = readHazik(d.osztaly)
                
                if diakHazik != None:
                    for g, e in enumerate(diakHazik):
                        a = self.query(".hazik")[g]
                        if a.title == "":
                            a.title = (
                                f"{e.targy} - Határidő: {e.hatarido}"
                            )
                            a.display = True
                        
                            self.query(".hazikContent")[g].update(e.feladat)
                else:
                    self.query_one("#diakHazik").update(
                        "Nincsenek feljegyzett házi feladatok."
                    )

        # tanár bejelentkezés
        for t in tanarok:
            if t.email == email and t.jelszo == password:
                self.query_one("#loginScreen").display = False
                self.query_one("#tanarScreen").display = True

                text = "\nHázi feladatok\n\n[Új feljegyzés]\n\n\nOsztály ("
                for i, a in enumerate(t.osztalyok):
                    if i != 0:
                        text += f", {a}"
                    else:
                        text += a

                text += "):"
                self.query_one("#tanarHazikLabel").update(text)
                self.query_one("#tanarLoginLabel").update(
                    f"Bejelentkezve: {t.nev} (tanár)"
                )
                self.query_one("#targyak").update(
                    f"Bukásra álló diákok: {Tanarok_bukoosztalyai(t.nev)}"
                )

    # handle email, password change
    @on(Input.Changed, "#email")
    def changeEmail(self, event: Input.Changed):
        global email
        email = event.value

    @on(Input.Changed, "#password")
    def changePassword(self, event: Input.Changed):
        global password
        password = event.value

    @on(Select.Changed, "#diakJegyekSelect")
    def select_changed(self, event: Select.Changed) -> None:
        for d in diakok:
            if d.email == email:
                string = ""
                atlag = 0
                for i, x in enumerate(d.jegyek[event.value]):
                    if i == 0:
                        string += f"{str(x)}"
                    else:
                        string += f", {str(x)}"

                    atlag += x
                atlag = atlag / len(d.jegyek[event.value])
                self.query_one("#diakJegyek").display = True
                self.query_one("#diakJegyek").update(f"{string}\n\nÁtlag: {atlag:.2f}")


# validate email, password
def bad_e(value: str) -> bool:
    try:
        for d in diakok:
            if d.email == value:
                return True
        for t in tanarok:
            if t.email == value:
                return True
    except ValueError:
        return False


def bad_p(value: str) -> bool:
    try:
        for d in diakok:
            if d.jelszo == value and d.email == email:
                return True
        for t in tanarok:
            if t.jelszo == value and t.email == email:
                return True
    except ValueError:
        return False


def bad_class(value: str) -> bool:
    try:
        for d in diakok:
            if d.osztaly == value:
                return True
    except ValueError:
        return False


def date(value: str) -> bool:
    try:
        splitted = value.strip().split(".")
        if len(splitted) == 3:
            if (len(splitted[0]) == 4) and (splitted[0].isnumeric()):
                if (len(splitted[1]) == 2) and (splitted[1].isnumeric()):
                    if (len(splitted[2]) == 2) and (splitted[2].isnumeric()):

                        return True
    except ValueError:
        return False


# run app
if __name__ == "__main__":
    KretaApp().run()
