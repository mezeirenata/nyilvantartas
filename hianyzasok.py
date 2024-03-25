class Hianyzas:
    def __init__(self, nev, idotartam, datum, igazolt) -> None:
        self.nev = nev
        self.idotartam = idotartam
        self.datum = datum
        self.igazolt = igazolt


def readHianyzasok(diaknev):
    hianyzasok = []
    f = open("csv/hazik.csv", "r", encoding="utf-8")
    f.readline()
    for line in f:
        hianyzas = line.strip().split(";")
        hianyzasok.append(Hianyzas(hianyzas[0], hianyzas[1], hianyzas[2], hianyzas[3]))
    f.close()

    diakHianyzasok = []
    for h in hianyzasok:
        if h.nev == diaknev:
            diakHianyzasok.append(h)

    if diakHianyzasok != []:
        return diakHianyzasok
    else:
        return None
