from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function
from textual.widgets import Input, Label, Pretty, Button
from main import diakok


class InputApp(App):
    
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
    Label {
        margin: 1 2;
        color: blue;
    }
    Pretty {
        margin: 1 2;
    }
    #login {
        margin-left: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Kréta 2.0")
        yield Input(
            placeholder="Email",
            validators=[Function(bad_e)],
            id="email"
        )
        yield Input(
            placeholder="Jelszó",
            validators=[Function(bad_j)],
            password=True,
            id="jelszo"
        )
        yield Button(
            label="Bejelentkezés",
            id="login"
        )
        yield Label(id="a")


    @on(Input.Submitted)
    def login(self, event: Input.Submitted) -> None:
        for d in diakok:
            if d.email == event.value:
                self.query_one("#a").update(d.nev)
    
                

    
        


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

app = InputApp()

if __name__ == "__main__":
    app.run()