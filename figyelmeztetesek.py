class Figyelmeztetes:
    def __init__(self, nev, tipus, fokozat, datum, megjegyzes) -> None:
        self.nev = nev
        self.tipus = tipus
        self.fokozat = fokozat
        self.datum = datum
        self.megjegyzes = megjegyzes


def readFigyelmeztetesek(diaknev):
    figyelmeztetesek = []
    f = open("csv/figyelmeztetesek.csv", "r", encoding="utf-8")
    f.readline()
    lines = f.readlines()

    figyelm = []
    for line in lines:
        line = line.strip()

        if line == "END":
            megjegyzes = ""
            for x, h in enumerate(figyelm[4:]):
                if x != 0:
                    megjegyzes += f"\n{h}"
                else:
                    megjegyzes += f"{h}"

            figyelmeztetesek.append(Figyelmeztetes(figyelm[0], figyelm[1], figyelm[2], figyelm[3], megjegyzes))
            figyelm = []

        else:
            figyelm.append(line)

    f.close()

    diakfigyelmeztetesek = []
    for h in figyelmeztetesek:
        if h.nev == diaknev:

            diakfigyelmeztetesek.append(h)

    if diakfigyelmeztetesek != []:
        return diakfigyelmeztetesek
    else:
        return None
