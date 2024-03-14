class Tanar:
    def __init__(self, sor: str) -> None:
        data = sor.strip().split(";")
        self.nev = data[0]
        self.osztalyok = self.lista(data[1])
        self.email = data[2]
        self.jelszo = data[3]
        self.targyak = self.lista(data[4])

    def lista(self, data):
        splitted = data.strip().split(",")
        lista = []
        for s in splitted:
            lista.append(s)
        return lista


tanarok: list[Tanar] = []


def readFile():
    f = open("csv/tanarok.csv", "r", encoding="utf-8")
    f.readline()
    for sor in f:
        tanarok.append(Tanar(sor))
    f.close()


readFile()
