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
    Checkbox,
)
from textual.containers import Horizontal, Center, Vertical
from diak import *
from tanar import *
from opciok import *
from hazik import *
from hianyzasok import *
from figyelmeztetesek import *

# tantárgyak listája
TARGYAK = list(diakok[0].jegyek)
OSZTALYOK = []
for d in diakok:
    if d.osztaly not in OSZTALYOK:
        OSZTALYOK.append(d.osztaly)
OSZTALYOK.sort()

IDOTARTAMOK = []
for i in range(10):
    if i != 0:
        IDOTARTAMOK.append(f"{str(i*5)} perc")
TIPUSOK = ["Szaktanári", "Osztályfőnöki", "Igazgatói"]
FOKOZATOK = ["Figyelmeztetés", "Intő", "Megrovás"]


# app
class KretaApp(App):

    CSS = """
    Screen {
        background: rgba(0, 128, 255, 0.1);
    }
    Input.-valid {
        border: tall $success 60%;
    }
    Input.-valid:focus {
        border: tall $success;
    }
    Input {
        width: 60%;
        margin-bottom: 2;
    }
    #tanarHazikInputHatar, #tanarHianyzasokDiaknev, #tanarHianyzasokDatumInput, #tanarHianyzasokIdotartamSelect, #tanarFigyelmDiaknev, #tanarFigyelmTipusSelect, #tanarFigyelmFokSelect, #tanarFigyelmInputDatum {
        width: 20%;
    }
    .centerCont {
        align: center middle;
    }
    .btn {
        text-style: none;
        margin: 1;
        margin-left: 3;
        border: round white;
        background: rgba(0,0,0,0);
    }
    .loginLabel {
        margin: 2 3;
        color: auto;
        background: white 10%;
        padding: 1;
        border: round white;
    }
    .label {
        margin-left: 3;
        margin-top: 1;
        margin-bottom: 1;
    }
    #diakJegyek {
        margin-top: 2;
        margin-left: 6;
        background: green 15%;
        color: auto;
        padding: 1 3;
        border: round green;
    }
    #diakJegyekSelect, #tanarHazikSelect {
        width: 35%;
        margin-left: 3;
        margin-bottom: 1;
    }
    #logoutBtn {
        background: red 30%;
        border: round red;
        color: auto;
    }
    Collapsible {
        border: round white;
    }
    #logoutBtn:hover {
        background: red 20%;
    }
    .btn:hover {
        background: rgba(0,0,0,0.4);
    }
    .hazikContent, .figyelmContent {
        height: 15;
    }
    #tanarHazikArea, #tanarFigyelmArea {
        width: 50%;
        height: 10;
        margin-left: 3;
    }
    #tanarHaziView {
        overflow: auto;
    }
    #tanarHazikInputOsztaly, #tanarJegyekSelectOsztaly, #tanarErdemjegySelect {
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
    #diakHazik, #diakFigyelm, #diakHianyzasok {
        margin-left: 3;
    }
    .btns, #loginScreen {
        border: round white;
    }
    #loginInputs {
        border: round white;
        margin-left: 50;
        margin-right: 50;
        margin-top: 10;
        margin-bottom: 10;
    }
    .success {
        color: green;
    }
    .fail {
        color: red;
    }
    #tanarHazikSuccessLabel, #tanarJegyFeljegyzesSuccessLabel, #tanarFigyelmSuccessLabel, #tanarHianyzasokSuccessLabel {
        margin-top: 1;
        margin-left: 3;
    }
    .hazik, .figyelm, .hianyzas {
        margin-left: 4;
        margin-top: 1;
        width: 50%;
    }
    .screen {
        width: 35%;
    }
    Checkbox {
        width: 50;
        border: round white;
        margin-left: 3;
        background: rgba(0,0,0,0);
    }
    Select {
        width: 40%;
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
            Vertical(
                Vertical(Label("Üdvözöljük!"), classes="centerCont"),
                Vertical(
                    Input(
                        placeholder="Email", validators=[Function(bad_e)], id="email"
                    ),
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
                id="loginInputs",
            ),
            id="loginScreen",
        )

        # diák nézet
        yield Horizontal(
            Vertical(
                Button("Kijelentkezés", id="logoutBtn", classes="btn"),
                Label("", classes="loginLabel", id="diakLoginLabel"),
                Button("Órarend", id="diakOrarendBtn", classes="btn"),
                Button("Jegyek", id="diakJegyekBtn", classes="btn"),
                Button("Házi feladatok", id="diakHaziBtn", classes="btn"),
                Button("Figyelmeztetések", id="diakFigyelmBtn", classes="btn"),
                Button("Hiányzások", id="diakHianyzasBtn", classes="btn"),
                classes="btns screen",
            ),
            Vertical(
                Label("\nÓrarend", id="diakOrarendLabel", classes="label"),
                DataTable(id="diakOrarend", zebra_stripes=True),
                id="diakOrarendView",
                classes="overflow",
            ),
            Vertical(
                Label("\nHiányzások", id="diakHianyzasLabel", classes="label"),
                Label(id="diakHianyzasok"),
                Collapsible(
                    Label("", classes="hianyzasContent"),
                    Button("Igazolás", classes="btn label diakIgazolasBtn"),
                    collapsed=True,
                    title="",
                    classes="hianyzas",
                ),
                Collapsible(
                    Label("", classes="hianyzasContent"),
                    Button("Igazolás", classes="btn label diakIgazolasBtn"),
                    collapsed=True,
                    title="",
                    classes="hianyzas",
                ),
                Collapsible(
                    Label("", classes="hianyzasContent"),
                    Button("Igazolás", classes="btn label diakIgazolasBtn"),
                    collapsed=True,
                    title="",
                    classes="hianyzas",
                ),
                Collapsible(
                    Label("", classes="hianyzasContent"),
                    Button("Igazolás", classes="btn label diakIgazolasBtn"),
                    collapsed=True,
                    title="",
                    classes="hianyzas",
                ),
                Collapsible(
                    Label("", classes="hianyzasContent"),
                    Button("Igazolás", classes="btn label diakIgazolasBtn"),
                    collapsed=True,
                    title="",
                    classes="hianyzas",
                ),
                Collapsible(
                    Label("", classes="hianyzasContent"),
                    Button("Igazolás", classes="btn label diakIgazolasBtn"),
                    collapsed=True,
                    title="",
                    classes="hianyzas",
                ),
                id="diakHianyzasView",
                classes="overflow",
            ),
            Vertical(
                Label("\nFigyelmeztetések", id="diakFigyelmLabel", classes="label"),
                Label("", id="diakFigyelm"),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                Collapsible(
                    TextArea(
                        "", classes="figyelmContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="figyelm",
                ),
                id="diakFigyelmView",
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
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
                    collapsed=True,
                    title="",
                    classes="hazik",
                ),
                Collapsible(
                    TextArea(
                        "", classes="hazikContent", read_only=True, soft_wrap=True
                    ),
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
                Button("Új házi feladat", id="tanarHaziBtn", classes="btn"),
                Button("Új érdemjegy", id="tanarJegyekBtn", classes="btn"),
                Button("Új hiányzás", id="tanarHianyzasBtn", classes="btn"),
                Button("Új figyelmeztetés", id="tanarFigyelmBtn", classes="btn"),
                Pretty("", id="targyak"),
                classes="btns screen",
            ),
            Vertical(
                Label(
                    "Új hiányzás feljegyzése\n\n\nDiák neve:",
                    id="tanarHianyzasLabel",
                    classes="label",
                ),
                Input(
                    placeholder="Példa Béla",
                    validators=[Function(bad_nev)],
                    id="tanarHianyzasokDiaknev",
                    classes="label",
                ),
                Label(
                    "Hiányzás időtartama:",
                    id="tanarHianyzasokIdotartam",
                    classes="label",
                ),
                Select(
                    ((line, line) for line in IDOTARTAMOK),
                    allow_blank=False,
                    value="5 perc",
                    id="tanarHianyzasokIdotartamSelect",
                    classes="label",
                ),
                Label("Dátum: ", id="tanarHianyzasokDatum", classes="label"),
                Input(
                    placeholder="YYYY.MM.DD.",
                    validators=[Function(date)],
                    id="tanarHianyzasokDatumInput",
                    classes="label",
                    max_length=11,
                ),
                Button(
                    "Feljegyzés", id="tanarHianyzasokFeljegyzesBtn", classes="btn label"
                ),
                Label("", id="tanarHianyzasokSuccessLabel", classes="label"),
                id="tanarHianyzasView",
                classes="overflow",
            ),
            Vertical(
                Label(
                    "Új figyelmeztetés feljegyzése\n\n\nDiák neve:",
                    id="tanarFigyelmLabel",
                    classes="label",
                ),
                Input(
                    placeholder="Példa Béla",
                    validators=[Function(bad_nev)],
                    id="tanarFigyelmDiaknev",
                    classes="label",
                ),
                Label(
                    "Típus:",
                    id="tanarFigyelmTipus",
                    classes="label",
                ),
                Select(
                    ((line, line) for line in TIPUSOK),
                    allow_blank=False,
                    value="Szaktanári",
                    id="tanarFigyelmTipusSelect",
                    classes="label",
                ),
                Label(
                    "Fokozat:",
                    id="tanarFigyelmFok",
                    classes="label",
                ),
                Select(
                    ((line, line) for line in FOKOZATOK),
                    allow_blank=False,
                    value="Figyelmeztetés",
                    id="tanarFigyelmFokSelect",
                    classes="label",
                ),
                Label("Dátum:", classes="label"),
                Input(
                    placeholder="YYYY.MM.DD.",
                    validators=[Function(date)],
                    id="tanarFigyelmInputDatum",
                    classes="label",
                    max_length=11,
                ),
                Label("Megjegyzés: ", id="tanarFigyelmMegjegy", classes="label"),
                TextArea(
                    id="tanarFigyelmArea", soft_wrap=True, show_line_numbers=False
                ),
                Button(
                    "Feljegyzés", id="tanarFigyelmFeljegyzesBtn", classes="btn label"
                ),
                Label("", id="tanarFigyelmSuccessLabel", classes="label"),
                id="tanarFigyelmView",
                classes="overflow",
            ),
            Vertical(
                Label(
                    "Új jegy feljegyzése\n\n\nOsztály:",
                    id="tanarJegyekLabel",
                    classes="label",
                ),
                Select(
                    ((line, line) for line in OSZTALYOK),
                    id="tanarJegyekSelectOsztaly",
                    allow_blank=False,
                    value="10B",
                    classes="label",
                ),
                Label("Diákok:", classes="label"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Checkbox("", classes="tanarJegyekCheckbox"),
                Label("Tantárgy:", classes="label"),
                Select(
                    ((line, line) for line in TARGYAK),
                    id="tanarJegyekSelect",
                    allow_blank=False,
                    value="Történelem",
                    classes="label",
                ),
                Label("Érdemjegy:", classes="label"),
                Select(
                    ((line, line) for line in ["5", "4", "3", "2", "1"]),
                    id="tanarErdemjegySelect",
                    allow_blank=False,
                    value="5",
                    classes="label",
                ),
                Button("Feljegyzés", classes="label btn", id="tanarJegyFeljegyzesBtn"),
                Label("", id="tanarJegyFeljegyzesSuccessLabel", classes="label"),
                id="tanarJegyekView",
                classes="overflow",
            ),
            Vertical(
                Label("", id="tanarHazikLabel", classes="label"),
                Select(
                    ((line, line) for line in OSZTALYOK),
                    id="tanarHazikInputOsztaly",
                    allow_blank=False,
                    value="10B",
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
                    placeholder="YYYY.MM.DD.",
                    validators=[Function(date)],
                    id="tanarHazikInputHatar",
                    classes="label",
                    max_length=11,
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
        self.query_one("#diakHianyzasView").display = False
        self.query_one("#diakFigyelmView").display = False

        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarHianyzasView").display = False
        self.query_one("#tanarJegyekView").display = False
        self.query_one("#tanarFigyelmView").display = False

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
        self.query_one("#diakHianyzasView").display = False
        self.query_one("#diakFigyelmView").display = False
        self.query_one("#tanarHianyzasView").display = False
        self.query_one("#tanarJegyekView").display = False
        self.query_one("#tanarHaziView").display = False

    @on(Button.Pressed, "#diakOrarendBtn")
    def diaOrarend(self, event: Button.Pressed) -> None:
        self.query_one("#diakHianyzasView").display = False
        self.query_one("#diakOrarendView").display = True
        self.query_one("#diakHaziView").display = False
        self.query_one("#diakFigyelmView").display = False
        self.query_one("#diakJegyekView").display = False

    @on(Button.Pressed, "#diakJegyekBtn")
    def diakJegyek(self, event: Button.Pressed) -> None:
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakHianyzasView").display = False
        self.query_one("#diakFigyelmView").display = False
        self.query_one("#diakHaziView").display = False
        self.query_one("#diakJegyekView").display = True

    @on(Button.Pressed, "#diakHaziBtn")
    def diakHazik(self, event: Button.Pressed) -> None:
        self.query_one("#diakFigyelmView").display = False
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakHianyzasView").display = False
        self.query_one("#diakHaziView").display = True
        self.query_one("#diakJegyekView").display = False

    @on(Button.Pressed, "#diakHianyzasBtn")
    def diakHianyzas(self, event: Button.Pressed) -> None:
        self.query_one("#diakFigyelmView").display = False
        self.query_one("#diakHianyzasView").display = True
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakHaziView").display = False
        self.query_one("#diakJegyekView").display = False

    @on(Button.Pressed, "#diakFigyelmBtn")
    def diakFigyelm(self, event: Button.Pressed) -> None:
        self.query_one("#diakHianyzasView").display = False
        self.query_one("#diakFigyelmView").display = True
        self.query_one("#diakOrarendView").display = False
        self.query_one("#diakHaziView").display = False
        self.query_one("#diakJegyekView").display = False

    @on(Button.Pressed, "#tanarJegyekBtn")
    def tanarJegyek(self, event: Button.Pressed) -> None:
        self.query_one("#tanarHianyzasView").display = False
        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarFigyelmView").display = False
        self.query_one("#tanarJegyekView").display = True
        self.query_one("#tanarJegyFeljegyzesSuccessLabel").display = False

    @on(Button.Pressed, "#tanarHianyzasBtn")
    def tanarHianyzasok(self, event: Button.Pressed) -> None:
        self.query_one("#tanarHianyzasView").display = True
        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarFigyelmView").display = False
        self.query_one("#tanarJegyekView").display = False
        self.query_one("#tanarHianyzasokSuccessLabel").display = False

    @on(Button.Pressed, "#tanarFigyelmBtn")
    def tanarFigyelm(self, event: Button.Pressed) -> None:
        self.query_one("#tanarHianyzasView").display = False
        self.query_one("#tanarFigyelmView").display = True
        self.query_one("#tanarHaziView").display = False
        self.query_one("#tanarJegyekView").display = False
        self.query_one("#tanarFigyelmSuccessLabel").display = False

    @on(Button.Pressed, "#tanarHaziBtn")
    def tanarHazik(self, event: Button.Pressed) -> None:
        self.query_one("#tanarHianyzasView").display = False
        self.query_one("#tanarHaziView").display = True
        self.query_one("#tanarFigyelmView").display = False
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

    @on(Button.Pressed, "#tanarFigyelmFeljegyzesBtn")
    def tanarFigyelmFeljegyzes(self, event: Button.Pressed) -> None:
        nev = self.query_one("#tanarFigyelmDiaknev").value
        tipus = self.query_one("#tanarFigyelmTipusSelect").value
        fokozat = self.query_one("#tanarFigyelmFokSelect").value
        datum = self.query_one("#tanarFigyelmInputDatum").value
        megjegyzes = self.query_one("#tanarFigyelmArea").text
        label = self.query_one("#tanarFigyelmSuccessLabel")
        label.display = True
        if (nev != "") and (datum != ""):
            f = open("csv/figyelmeztetesek.csv", "a", encoding="utf-8")
            f.write(f"{nev}\n{tipus}\n{fokozat}\n{datum}\n{megjegyzes}\nEND\n")
            f.close()
            label.update("Sikeres feljegyzés!")
            label.classes = "success"
        else:
            label.update("Sikertelen feljegyzés!\nTöltsön ki minden mezőt!")
            label.classes = "fail"

    @on(Button.Pressed, "#tanarHianyzasokFeljegyzesBtn")
    def tanarHianyzasFeljegyzes(self, event: Button.Pressed) -> None:
        label = self.query_one("#tanarHianyzasokSuccessLabel")
        nev = self.query_one("#tanarHianyzasokDiaknev").value
        datum = self.query_one("#tanarHianyzasokDatumInput").value
        idotartam = self.query_one("#tanarHianyzasokIdotartamSelect").value
        label.display = True
        if (datum != "") and (nev != ""):
            f = open("csv/hianyzasok.csv", "a", encoding="utf-8")
            f.write(f"{nev};{idotartam};{datum};False\n")
            f.close()
            label.update("Sikeres feljegyzés!")
            label.classes = "success"
        else:
            label.update("Sikertelen feljegyzés!\nTöltsön ki minden mezőt!")
            label.classes = "fail"

    @on(Button.Pressed, "#tanarHazikBtnReset")
    def tanarHazikFeljegyzesReset(self, event: Button.Pressed) -> None:
        self.query_one("#tanarHazikInputOsztaly").value = "10B"
        self.query_one("#tanarHazikSelect").value = "Történelem"
        self.query_one("#tanarHazikInputHatar").value = ""
        self.query_one("#tanarHazikArea").text = ""
        self.query_one("#tanarHazikSuccessLabel").update("")

    @on(Button.Pressed, "#tanarJegyFeljegyzesBtn")
    def tanarJegyFeljegyzes(self, event: Button.Pressed) -> None:

        label = self.query_one("#tanarJegyFeljegyzesSuccessLabel")
        label.display = True
        filled = False
        for a in self.query(".tanarJegyekCheckbox"):
            if a.value == True:
                filled = True
        if filled:
            for a in self.query(".tanarJegyekCheckbox"):
                if a.value == True:
                    for d in diakok:
                        if d.nev == str(a.label):
                            targy = self.query_one("#tanarJegyekSelect").value
                            jegy = self.query_one("#tanarErdemjegySelect").value
                            d.addJegy(targy, jegy)
                            label.update("Sikeres feljegyzés!")
                            label.classes = "success"
        else:
            label.update("Sikertelen feljegyzés!\nVálasszon ki legalább egy diákot!")
            label.classes = "fail"

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

                for a in self.query(".hianyzas"):
                    a.display = False

                osszes = readHianyzasok(d.nev)

                def igazolt(boolean):
                    if boolean == "True":
                        return "Igen"
                    else:
                        return "Nem"

                if osszes != None:
                    self.query_one("#diakHianyzasok").update("")
                    for g, e in enumerate(osszes):
                        a = self.query(".hianyzas")[g]
                        a.title = f"{e.datum}"
                        a.display = True
                        self.query(".hianyzasContent")[g].update(
                            f"{e.idotartam}\nIgazolt: {igazolt(e.igazolt)}"
                        )
                else:
                    self.query_one("#diakHianyzasok").update(
                        "Nincsenek feljegyzett hiányzások."
                    )

                for a in self.query(".figyelm"):
                    a.display = False

                osszes = readFigyelmeztetesek(d.nev)

                if osszes != None:
                    self.query_one("#diakFigyelm").update("")
                    for g, e in enumerate(osszes):
                        a = self.query(".figyelm")[g]
                        a.title = f"{e.tipus} {e.fokozat} - Dátum: {e.datum}"
                        a.display = True
                        self.query(".figyelmContent")[g].text = e.megjegyzes
                else:
                    self.query_one("#diakFigyelm").update("Nincsenek figyelmeztetések.")

                for a in self.query(".hazik"):
                    a.display = False

                osszes = readHazik(d.osztaly)

                if osszes != None:
                    self.query_one("#diakHazik").update("")
                    for g, e in enumerate(osszes):
                        a = self.query(".hazik")[g]
                        a.title = f"{e.targy} - Határidő: {e.hatarido}"
                        a.display = True
                        self.query(".hazikContent")[g].text = e.feladat
                else:
                    self.query_one("#diakHazik").update(
                        "Nincsenek feljegyzett házi feladatok."
                    )

        # tanár bejelentkezés
        for t in tanarok:
            if t.email == email and t.jelszo == password:
                self.query_one("#loginScreen").display = False
                self.query_one("#tanarScreen").display = True

                text = "Új házi feladat feljegyzése\n\n\nOsztály ("
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
                for a in self.query(".tanarJegyekCheckbox"):
                    a.display = False
                    a.value = False
                osztalyDiakjai = []
                osztaly = self.query_one("#tanarJegyekSelectOsztaly").value
                for x in diakok:
                    if x.osztaly == osztaly:
                        osztalyDiakjai.append(x.nev)

                for g, e in enumerate(osztalyDiakjai):
                    a = self.query(".tanarJegyekCheckbox")[g]
                    a.label = e
                    a.display = True

    # handle change
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

    @on(Select.Changed, "#tanarJegyekSelectOsztaly")
    def tanarJegyekSelect_changed(self, event: Select.Changed) -> None:
        self.query_one("#tanarJegyFeljegyzesSuccessLabel").display = False
        for a in self.query(".tanarJegyekCheckbox"):
            a.display = False
            a.value = False
        osztalyDiakjai = []
        osztaly = self.query_one("#tanarJegyekSelectOsztaly").value
        for x in diakok:
            if x.osztaly == osztaly:
                osztalyDiakjai.append(x.nev)

        for g, e in enumerate(osztalyDiakjai):
            a = self.query(".tanarJegyekCheckbox")[g]
            a.label = e
            a.display = True


# validate input
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


def bad_nev(value: str) -> bool:
    try:
        for d in diakok:
            if d.nev == value:
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


def date(value: str) -> bool:
    try:
        splitted = value.strip().split(".")
        if len(splitted) == 4:
            if (len(splitted[0]) == 4) and (splitted[0].isnumeric()):
                if (len(splitted[1]) == 2) and (splitted[1].isnumeric()):
                    if (len(splitted[2]) == 2) and (splitted[2].isnumeric()):
                        if splitted[3] == "":
                            return True
    except ValueError:
        return False


# run app
if __name__ == "__main__":
    KretaApp().run()
