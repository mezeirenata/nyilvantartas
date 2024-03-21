class Diak:
    def __init__(self, sor) -> None:
        data = sor.strip().split(";")
        self.nev = data[0]
        self.osztaly = data[1]
        self.email = data[2]
        self.jelszo = data[3]
        self.jegyek = self.jegyekDict()
        self.tan_atlag = self.tanAtlag()
        self.orarend = self.orarendParser()
        self.osztondij = self.osztondij()

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
                global d
                d = dictionary
            else:
                if splitted[0] == self.nev:
                    for x, s in enumerate(splitted[1:]):
                        splitted2 = s.split(",")
                        for a in splitted2:
                            keys = list(dictionary)
                            dictionary[keys[x]].append(int(a))

        f.close()
        return dictionary

    def addJegy(self, targy, jegy):
        for a in self.jegyek.keys():
            if a == targy:
                self.jegyek[targy].append(int(jegy))
        f = open("csv/jegyek.csv", "w+", encoding="utf-8")
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            splitted = line.split(";")
            if splitted[0] == self.nev:
                pass
        f.close()

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
            ["1.", "-", "-", "-", "-", "-"],
            ["2.", "-", "-", "-", "-", "-"],
            ["3.", "-", "-", "-", "-", "-"],
            ["4.", "-", "-", "-", "-", "-"],
            ["5.", "-", "-", "-", "-", "-"],
            ["6.", "-", "-", "-", "-", "-"],
            ["7.", "-", "-", "-", "-", "-"],
        ]

        f = open("csv/orarendek.csv", "r", encoding="utf-8")
        f.readline()
        for sor in f:
            splitted = sor.strip().split(";")
            targyak = splitted[2].split(",")
            if splitted[0] == self.osztaly:
                match splitted[1]:
                    case "Hétfő":
                        for i, s in enumerate(targyak):
                            ROWS[i + 1][1] = s

                    case "Kedd":
                        for i, s in enumerate(targyak):
                            ROWS[i + 1][2] = s

                    case "Szerda":
                        for i, s in enumerate(targyak):
                            ROWS[i + 1][3] = s

                    case "Csütörtök":
                        for i, s in enumerate(targyak):
                            ROWS[i + 1][4] = s

                    case "Péntek":
                        for i, s in enumerate(targyak):
                            ROWS[i + 1][5] = s

        f.close()

        return ROWS

    def osztondij(self):
        dij = 0
        if ("9" in self.osztaly) or ("10" in self.osztaly):
            dij = "8000 Ft"
        else:
            a = self.tan_atlag
            if a > 4.49:
                dij = "59000 Ft"
            elif a > 4:
                dij = "42000 Ft"
            elif a > 3:
                dij = "25000 Ft"
            elif a > 2:
                dij = "8000 Ft"
            else:
                dij = "Nincs"

        return dij


diakok: list[Diak] = []


def readFile():
    f = open("csv/diakok.csv", "r", encoding="utf-8")
    f.readline()
    for sor in f:
        diakok.append(Diak(sor))
    f.close()


readFile()
