class Diak:
    def __init__(self, sor) -> None:
        data = sor.strip().split(";")
        self.nev = data[0]
        self.osztaly = data[1]
        self.email = data[2]
        self.jelszo = data[3]
        self.osztondij = int(data[4])
        self.jegyek = self.jegyekDict()
        self.tan_atlag = self.tanAtlag()
        self.orarend = self.orarendParser()

    def jegyekDict(self):
        dictionary = {}
        f = open("csv/jegyek.csv", "r", encoding="utf-8")
        for i, sor in enumerate(f):
            splitted = sor.strip().split(";")
            if i == 0:
                targyak = sor.strip().split(";")
                for t in targyak:
                    if t != "Név":
                        dictionary[t] = []
            else:
                if splitted[0] == self.nev:
                    for x, s in enumerate(splitted[1:]):
                        splitted2 = s.split(",")
                        for a in splitted2:
                            keys = list(dictionary)
                            dictionary[keys[x]].append(int(a))

        f.close()
        return dictionary

    def tanAtlag(self):
        tan_atlag = 0
        atlag_lista = []
        for lista in self.jegyek.values():
            atlag = 0
            for x in lista:
                atlag += x
            atlag = atlag / len(lista)
            atlag_lista.append(atlag)
        for i in atlag_lista:
            tan_atlag += i
        tan_atlag = tan_atlag / len(atlag_lista)

        return tan_atlag

    def orarendParser(self):
        ROWS = [
            [f"{self.osztaly}", "Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"],
            [1, "", "", "", "", ""],
            [2, "", "", "", "", ""],
            [3, "", "", "", "", ""],
            [4, "", "", "", "", ""],
            [5, "", "", "", "", ""],
            [6, "", "", "", "", ""],
            [7, "", "", "", "", ""],
        ]

        f = open("csv/orarendek.csv", "r", encoding="utf-8")
        f.readline()
        for sor in f:
            splitted = sor.strip().split(";")
            if splitted[0] == self.osztaly:
                match splitted[1]:
                    case "hetfo":
                        for i, s in enumerate(splitted[2:]):
                            ROWS[i + 1][1] = s

                    case "kedd":
                        for i, s in enumerate(splitted[2:]):
                            ROWS[i + 1][2] = s

                    case "szerda":
                        for i, s in enumerate(splitted[2:]):
                            ROWS[i + 1][3] = s

                    case "csutortok":
                        for i, s in enumerate(splitted[2:]):
                            ROWS[i + 1][4] = s

                    case "pentek":
                        for i, s in enumerate(splitted[2:]):
                            ROWS[i + 1][5] = s

        f.close()

        return ROWS


diakok: list[Diak] = []


def readFile():
    f = open("csv/diakok.csv", "r", encoding="utf-8")
    f.readline()
    for sor in f:
        diakok.append(Diak(sor))
    f.close()


readFile()
