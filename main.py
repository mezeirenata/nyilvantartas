from os import system as cmd

cmd("pip install textual")
from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function
from textual.widgets import Input, Label, Button, Header, Select, DataTable, Pretty
from textual.containers import Container
from diak import *
from tanar import *
from opciok import *


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
        width: 50%;
    }
    .centerCont {
        align: center middle;
    }
    .btn {
        text-style: none;
    }
    .loginLabel {
        margin: 2 3;
        color: auto;
        background: white 25%;
        padding: 1;
    }
    #jegyekLabel {
        margin-left: 3;
        margin-bottom: 1;
    }
    #jegyek {
        margin-top: 2;
        margin-left: 6;
        background: blue 30%;
        color: auto;
        padding: 1 3;
    }
    #jegyekSelect {
        width: 35%;
        margin-left: 3;
    }
    #logoutBtn {
        background: red 60%;
        color: auto;
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
        yield Container(
            Container(Label("Üdvözöljük!"), classes="centerCont"),
            Container(
                Input(placeholder="Email", validators=[Function(bad_e)], id="email"),
                classes="centerCont",
            ),
            Container(
                Input(
                    placeholder="Jelszó",
                    validators=[Function(bad_p)],
                    password=True,
                    id="password",
                ),
                classes="centerCont",
            ),
            Container(
                Button(label="Bejelentkezés", id="loginBtn", classes="btn"),
                classes="centerCont",
            ),
            Container(
                Button(label="Reset", id="resetBtn", classes="btn"),
                classes="centerCont",
            ),
            id="loginScreen",
        )

        yield Container(
            Button("Kijelentkezés", id="logoutBtn", classes="btn"),
            Label("", classes="loginLabel", id="diakLoginLabel"),
            Button("Órarend", id="orarendBtn", classes="btn"),
            Button("Jegyek", id="jegyekBtn", classes="btn"),
            Pretty("", id="osztondij"),
            id="diakScreen",
        )

        yield Container(
            Button("Kijelentkezés", id="logoutBtn", classes="btn"),
            Label("", classes="loginLabel", id="tanarLoginLabel"),
            Pretty("", id="targyak"),
            id="tanarScreen",
        )

        yield Container(DataTable(id="orarend"), id="orarendView")

        yield Container(
            Label("", id="jegyekLabel"),
            Select(
                ((line, line) for line in TARGYAK),
                id="jegyekSelect",
                allow_blank=False,
                value="Történelem",
            ),
            Label("", id="jegyek"),
            id="jegyekView",
        )

    def on_mount(self):
        self.query_one("#diakScreen").display = False
        self.query_one("#tanarScreen").display = False
        self.query_one("#orarendView").display = False
        self.query_one("#jegyekView").display = False
        self.title = "Kréta 2.0"

    # handle email, password change
    @on(Input.Changed, "#email")
    def changeEmail(self, event: Input.Changed):
        global email
        email = event.value

    @on(Input.Changed, "#password")
    def changePassword(self, event: Input.Changed):
        global password
        password = event.value

    @on(Select.Changed, "#jegyekSelect")
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
                self.query_one("#jegyek").display = True
                self.query_one("#jegyek").update(f"{string}\n\nÁtlag: {atlag:.2f}")

    # handle button presses
    @on(Button.Pressed, "#loginBtn")
    def login(self, event: Button.Pressed) -> None:
        # diák bejelentkezés
        for d in diakok:
            if d.email == email and d.jelszo == password:

                self.query_one("#loginScreen").display = False
                self.query_one("#diakScreen").display = True

                self.query_one("#diakLoginLabel").update(
                    f"Bejelentkezve: {d.nev} (diák)"
                )
                self.query_one("#jegyekLabel").update(
                    f"Jegyek\nTanulmányi átlag: {d.tan_atlag:.2f}"
                )
                self.query_one("#jegyek").display = False
                self.query_one("#osztondij").update(f"Ösztöndíj: {d.osztondij}")

        # tanár bejelentkezés
        for t in tanarok:
            if t.email == email and t.jelszo == password:
                self.query_one("#loginScreen").display = False
                self.query_one("#tanarScreen").display = True

                self.query_one("#tanarLoginLabel").update(
                    f"Bejelentkezve: {t.nev} (tanár)"
                )
                self.query_one("#targyak").update(
                    f"Bukásra álló diákok: {Tanarok_bukoosztalyai(t.nev)}"
                )

    @on(Button.Pressed, "#resetBtn")
    def reset(self, event: Button.Pressed) -> None:
        self.query_one("#email").value = ""
        self.query_one("#password").value = ""

    @on(Button.Pressed, "#logoutBtn")
    def logout(self, event: Button.Pressed) -> None:
        self.query_one("#loginScreen").display = True
        self.query_one("#diakScreen").display = False
        self.query_one("#tanarScreen").display = False
        self.query_one("#orarendView").display = False
        self.query_one("#jegyekView").display = False

    @on(Button.Pressed, "#orarendBtn")
    def orarend(self, event: Button.Pressed) -> None:
        self.query_one("#orarendView").display = True
        self.query_one("#jegyekView").display = False
        for d in diakok:
            if d.email == email:
                table: DataTable = self.query_one("#orarend")
                table.clear(True)
                table.add_columns(*d.orarend[0])
                table.add_rows(d.orarend[1:])

    @on(Button.Pressed, "#jegyekBtn")
    def jegyek(self, event: Button.Pressed) -> None:
        self.query_one("#orarendView").display = False
        self.query_one("#jegyekView").display = True


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


# run app
if __name__ == "__main__":
    KretaApp().run()
