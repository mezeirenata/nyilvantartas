class Hazi:
    def __init__(self, osztaly, targy, hatarido, feladat) -> None:
        self.osztaly = osztaly
        self.targy = targy
        self.hatarido = hatarido
        self.feladat = feladat


hazik = []


def readHazik(osztaly):
    f = open("csv/hazik.csv", "r", encoding="utf-8")
    f.readline()
    lines = f.readlines()

    hazi = []
    for line in lines:
        line = line.strip()

        if line == "END":
            feladat = ""
            for x, h in enumerate(hazi[3:]):
                if x != 0:
                    feladat += f"\n{h}"
                else:
                    feladat += f"{h}"

            hazik.append(Hazi(hazi[0], hazi[1], hazi[2], feladat))
            hazi = []

        else:
            hazi.append(line)

    f.close()

    diakHazik = []
    for h in hazik:
        if h.osztaly == osztaly:

            diakHazik.append(h)

    if diakHazik != []:
        return diakHazik
    else:
        return None
