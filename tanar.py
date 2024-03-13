class Tanar:
    def __init__(self, sor:str) -> None:
            data = sor.strip().split(";")
            self.nev = data[0]
            self.osztalyokat_tanit = data[1]
            self.email = data[2]
            self.jelszo = data[3]
            self.tantargyak = self.Tantargyak(data[4])
    
    def Tantargyak(self, tantargyak:str) -> list[str]:
        Tantargyakat_tanit: list[str] = []
        if "," in tantargyak:
            tantargyak.split(',')
            for x in tantargyak:
                 Tantargyakat_tanit.append(x)
        else:
             Tantargyakat_tanit.append(tantargyak)
        return Tantargyakat_tanit
        



tanarok: list[Tanar] = []


def readFile():
    f = open("csv/tanarok.csv", "r", encoding="utf-8")
    f.readline()
    for sor in f:
        tanarok.append(Tanar(sor))
    f.close()


readFile()