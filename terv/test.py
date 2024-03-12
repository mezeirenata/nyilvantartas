from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function
from textual.widgets import Input, Label, Pretty, Button, Header
from diak import *

diakok: list[Diak] = []

def readFile(filename):
    f = open(f"csv/{filename}", "r",encoding="utf-8")
    f.readline()
    for sor in f:
        diakok.append(Diak(sor))
    f.close()

readFile("diakok.csv")


class KretaApp(App):
    
    CSS = """
    Input.-valid {
        border: tall $success 60%;
    }
    Input.-valid:focus {
        border: tall $success;
    }
    Input {
        margin: 1 1;
    }
    #loginBtn {
        margin-left: 2;
    }
    #loginBtn:focus{
        text-style: none;
    }
    Header {
        color: red;
    }
    #loginLabel {
        margin: 2 3;
        color: auto;
        background: white 25%;
    }
    #jegyekLabel {
        margin: 2 3;
    }
    #jegyek {
        margin: 4 0;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(
            placeholder="Email",
            validators=[Function(bad_e)],
            id="email",
            value=""
        )
        yield Input(
            placeholder="Jelszó",
            validators=[Function(bad_j)],
            password=True,
            id="password",
            value=""
        )
        yield Button(
            label="Bejelentkezés",
            id="loginBtn"
        )

        yield Label("", id="loginLabel")
        yield Label("", id="jegyekLabel")
        yield Pretty(None, id="jegyek")
    
    def on_mount(self):
        self.title = "Kréta 2.0"
        

    global email
    global password
    email = ""
    password = ""

    @on(Input.Changed, "#email")
    def changeEmail(self, event: Input.Changed):
        global email
        email = event.value

    @on(Input.Changed, "#password")
    def changePassword(self, event: Input.Changed):
        global password
        password = event.value


    @on(Button.Pressed)
    def login(self, event: Button.Pressed) -> None:
        

        for d in diakok:
            if d.email == email and d.jelszo == password:
                self.query_one("#loginLabel").update(f"Bejelentkezve: {d.nev}")
                self.query_one("#jegyekLabel").update("Jegyek")

                self.query_one("#jegyek").update(d.jegyek)
            else:
                self.query_one("#jegyek").update(None)




    
    
        


def bad_e(value: str) -> bool:
    try:
        for d in diakok:
            if d.email == value:
                return True
    except ValueError:
        return False
    
def bad_j(value: str) -> bool:
    try:
        for d in diakok:
            if d.jelszo == value:
                return True
    except ValueError:
        return False


if __name__ == "__main__":
    KretaApp().run()